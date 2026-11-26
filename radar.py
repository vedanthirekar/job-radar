"""Job radar: check every watched company's job board, alert on new matching jobs.

Run every 10 minutes by GitHub Actions. State lives in state/seen.json.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import ats
import dashboard
import filters
from names import norm

ROOT = Path(__file__).parent
COMPANIES = ROOT / "companies.csv"
SPONSORS = ROOT / "data" / "sponsors.csv"
STATE = ROOT / "state" / "seen.json"
LOG = ROOT / "data" / "jobs_log.csv"
MAX_AGE = timedelta(hours=int(os.environ.get("MAX_AGE_HOURS", "72")))
MAX_ALERTS_PER_RUN = 15
WORKERS = 32
NTFY_SERVER = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")
NTFY_TOKEN = os.environ.get("NTFY_TOKEN", "")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

LOG_FIELDS = ["checked_at", "company", "title", "location", "url", "posted_at", "minutes_old",
              "alerted", "reason", "resume", "flags", "sponsor"]


def load_companies() -> list[dict]:
    if not COMPANIES.exists():
        return []
    with COMPANIES.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("ats") and r.get("slug")]
    seen, out = set(), []
    for r in rows:
        k = (r["ats"], r["slug"])
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


def load_sponsors() -> dict[str, dict]:
    if not SPONSORS.exists():
        return {}
    with SPONSORS.open(encoding="utf-8", newline="") as f:
        return {r["employer_norm"]: r for r in csv.DictReader(f)}


def sponsor_tag(company: str, sponsors: dict) -> str:
    if not sponsors:
        return ""
    n = norm(company)
    row = sponsors.get(n)
    if not row and n:
        # "snowplow" vs "snowplow analytics": pick the busiest employer starting with the name
        cands = [r for k, r in sponsors.items() if k.startswith(n + " ")]
        row = max(cands, key=lambda r: int(r["tech_lcas"]), default=None)
    if not row:
        return "No sponsor record"
    tech = int(row["tech_lcas"])
    perm = int(row.get("perm", 0) or 0)
    label = "Sponsors" if tech >= 3 else "Some sponsorship"
    extra = f", {perm} green card" if perm else ""
    return f"{label} ({tech} tech H-1B filings since FY{row.get('since_fy', '2025')}{extra})"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"boards": {}}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(exist_ok=True)
    # one line per board keeps git diffs small
    boards = state["boards"]
    lines = ["{", '"boards": {']
    items = sorted(boards.items())
    for i, (k, ids) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f"{json.dumps(k)}: {json.dumps(sorted(ids))}{comma}")
    lines += ["}", "}"]
    STATE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _post(body: str, headers: dict) -> None:
    if NTFY_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_TOKEN}"
    req = urllib.request.Request(f"{NTFY_SERVER}/{urllib.parse.quote(NTFY_TOPIC)}",
                                 data=body.encode("utf-8"), headers=headers, method="POST")
    try:
        urllib.request.urlopen(req, timeout=15).read()
    except Exception as e:
        print(f"ntfy failed: {e} (if 429, add an NTFY_TOKEN secret)", file=sys.stderr)


def notify(job: ats.Job, resume: str, flags: list[str], sponsor: str, minutes_old: int | None) -> None:
    age = f"{minutes_old} min ago" if minutes_old is not None else "just found"
    title = f"{job.company}: {job.title}"
    lines = [f"{job.location or 'Location not listed'} · posted {age}", f"Use: {resume}"]
    if sponsor:
        lines.append(sponsor)
    if flags:
        lines.append("Note: " + ", ".join(flags))
    body = "\n".join(lines)
    if DRY_RUN or not NTFY_TOPIC:
        print(f"[alert] {title}\n  {body.replace(chr(10), chr(10) + '  ')}\n  {job.url}")
        return
    _post(body, {
        "Title": title.encode("ascii", "ignore").decode()[:200],
        "Click": job.url,
        "Tags": "briefcase",
        "Priority": "high" if minutes_old is not None and minutes_old <= 60 else "default",
        "Actions": f"view, Apply, {job.url}",
    })


def notify_summary(extra: list[ats.Job]) -> None:
    if not extra:
        return
    names = "\n".join(f"{j.company}: {j.title}" for j in extra[:20])
    if DRY_RUN or not NTFY_TOPIC:
        print(f"[summary] {len(extra)} more\n{names}")
        return
    _post(names, {"Title": f"{len(extra)} more new matches", "Tags": "briefcase"})


def append_log(rows: list[dict]) -> None:
    if not rows:
        return
    LOG.parent.mkdir(exist_ok=True)
    new = not LOG.exists()
    with LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)


def main() -> int:
    t0 = time.time()
    companies = load_companies()
    sponsors = load_sponsors()
    state = load_state()
    boards = state["boards"]
    now = datetime.now(timezone.utc)
    print(f"{len(companies)} boards, {len(sponsors)} sponsor records")

    results: dict[str, list[ats.Job]] = {}
    failed = 0
    with ThreadPoolExecutor(WORKERS) as pool:
        futs = {pool.submit(ats.fetch_board, c["ats"], c["slug"], c.get("name", "")): c for c in companies}
        for fut in as_completed(futs):
            c = futs[fut]
            key = f'{c["ats"]}:{c["slug"]}'
            try:
                results[key] = fut.result()
            except Exception as e:
                failed += 1
                print(f"  fail {key}: {e}", file=sys.stderr)

    candidates: list[ats.Job] = []
    first_time = 0
    for key, jobs in results.items():
        ids_now = {j.job_id for j in jobs}
        if key not in boards:
            boards[key] = sorted(ids_now)      # new board: learn it quietly, no alerts
            first_time += 1
            continue
        old = set(boards[key])
        boards[key] = sorted(ids_now)         # closed jobs drop out; failed fetches keep old list
        candidates += [j for j in jobs if j.job_id not in old]

    log_rows, to_alert = [], []
    for job in candidates:
        ok, reason = filters.title_ok(job.title)
        if not ok:
            continue                           # don't log every sales role
        minutes_old = None
        if job.posted_at:
            minutes_old = max(0, int((now - job.posted_at).total_seconds() // 60))
        # Lever's date is when the job was created, which can be days before it went live.
        max_age = timedelta(days=21) if job.ats == "lever" else MAX_AGE
        if job.posted_at and now - job.posted_at > max_age:
            ok, reason = False, "old posting (repost or late add)"
        if job.ats == "lever" and minutes_old is not None and minutes_old > 24 * 60:
            minutes_old = None                 # shows "just found" instead of a misleading age
        if ok:
            ok, reason = filters.location_ok(job)
        if ok and job.ats == "greenhouse" and not job.description:
            try:
                job.description = ats.greenhouse_description(job.slug, job.job_id)
            except Exception as e:
                print(f"  desc fail {job.key}: {e}", file=sys.stderr)
        if ok:
            hit = filters.description_block(job.description)
            if hit:
                ok, reason = False, f"blocked: {hit}"
        resume = filters.pick_resume(job) if ok else ""
        flags = filters.flags_for(job) if ok else []
        sponsor = sponsor_tag(job.company, sponsors) if ok else ""
        log_rows.append({
            "checked_at": now.isoformat(timespec="minutes"), "company": job.company, "title": job.title,
            "location": job.location, "url": job.url,
            "posted_at": job.posted_at.isoformat(timespec="minutes") if job.posted_at else "",
            "minutes_old": "" if minutes_old is None else minutes_old,
            "alerted": "yes" if ok else "no", "reason": reason, "resume": resume,
            "flags": "; ".join(flags), "sponsor": sponsor,
        })
        if ok:
            to_alert.append((job, resume, flags, sponsor, minutes_old))

    # freshest first
    to_alert.sort(key=lambda x: x[4] if x[4] is not None else 0)
    for job, resume, flags, sponsor, mins in to_alert[:MAX_ALERTS_PER_RUN]:
        notify(job, resume, flags, sponsor, mins)
    notify_summary([x[0] for x in to_alert[MAX_ALERTS_PER_RUN:]])

    append_log(log_rows)
    save_state(state)
    dashboard.build()
    print(f"done in {time.time() - t0:.0f}s: {len(results)} ok, {failed} failed, {first_time} new boards, "
          f"{len(candidates)} new jobs, {len(to_alert)} alerts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
