"""Find which job system (Greenhouse, Lever, Ashby) each company uses.

Reads company names from candidates.txt (hand-picked) and
data/sponsor_candidates.txt (built by sponsors.py from H-1B filings),
tries likely board names on each system, and adds hits to companies.csv.

candidates.txt format: one company per line. Optional override:
    Company Name | ats:slug        e.g.  Snowplow | greenhouse:snowplow
Lines starting with # are ignored.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

import ats
from names import norm, slug_guesses

ROOT = Path(__file__).parent
COMPANIES = ROOT / "companies.csv"
HAND = ROOT / "candidates.txt"
FROM_SPONSORS = ROOT / "data" / "sponsor_candidates.txt"
PROBED = ROOT / "data" / "probed.json"
RETRY_MISSES_AFTER = timedelta(days=30)
WORKERS = int(os.environ.get("DETECT_WORKERS", "32"))
SYSTEMS = ["greenhouse", "ashby", "lever"]
FIELDS = ["name", "ats", "slug", "source", "added"]


def read_names(path: Path, source: str) -> list[tuple[str, str, str]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        override = ""
        if "|" in line:
            line, override = [p.strip() for p in line.split("|", 1)]
        out.append((line, source, override))
    return out


def probe(ats_name: str, slug: str, company: str, strict: bool):
    """Return number of jobs if the board exists, else None."""
    try:
        data = ats.http_get_json(ats.probe_url(ats_name, slug), retries=1)
    except ats.FetchError:
        return None
    if ats_name == "greenhouse":
        jobs = data.get("jobs") if isinstance(data, dict) else None
        if jobs is None:
            return None
        if strict and jobs:
            names = {norm(j.get("company_name", "")) for j in jobs[:5]}
            target = norm(company)
            if not any(n and (n == target or n.startswith(target) or target.startswith(n)) for n in names):
                return None
        return len(jobs)
    if ats_name == "ashby":
        jobs = data.get("jobs") if isinstance(data, dict) else None
        return len(jobs) if jobs else None
    if ats_name == "lever":
        return len(data) if isinstance(data, list) and data else None
    return None


def find_board(name: str, source: str, override: str):
    if override and ":" in override:
        a, s = override.split(":", 1)
        return name, a.strip(), s.strip(), source
    strict = source == "sponsors"
    guesses = slug_guesses(name, first_word=not strict)
    if strict:
        guesses = guesses[:2]          # exact name only, avoid look-alike boards
    for slug in guesses:
        for a in SYSTEMS:
            if probe(a, slug, name, strict) is not None:
                return name, a, slug, source
    return None


def main() -> int:
    today = date.today()
    existing = []
    if COMPANIES.exists():
        with COMPANIES.open(encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
    known_names = {norm(r["name"]) for r in existing}
    known_boards = {(r["ats"], r["slug"]) for r in existing}
    probed = json.loads(PROBED.read_text(encoding="utf-8")) if PROBED.exists() else {}

    todo = []
    for name, source, override in read_names(HAND, "hand") + read_names(FROM_SPONSORS, "sponsors"):
        n = norm(name)
        if not n or n in known_names:
            continue
        last = probed.get(n)
        if last and not override and date.fromisoformat(last) > today - RETRY_MISSES_AFTER:
            continue
        todo.append((name, source, override))
        known_names.add(n)
    print(f"probing {len(todo)} companies")

    added = []
    with ThreadPoolExecutor(WORKERS) as pool:
        futs = {pool.submit(find_board, *t): t for t in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            name, source, _ = futs[fut]
            try:
                hit = fut.result()
            except Exception as e:
                print(f"  error {name}: {e}", file=sys.stderr)
                continue
            if hit and (hit[1], hit[2]) not in known_boards:
                known_boards.add((hit[1], hit[2]))
                added.append({"name": hit[0], "ats": hit[1], "slug": hit[2], "source": hit[3],
                              "added": today.isoformat()})
                print(f"  + {hit[0]} -> {hit[1]}:{hit[2]}")
            elif not hit:
                probed[norm(name)] = today.isoformat()
            if i % 200 == 0:
                print(f"  ...{i}/{len(todo)}")

    rows = existing + added
    rows.sort(key=lambda r: r["name"].lower())
    with COMPANIES.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    PROBED.parent.mkdir(exist_ok=True)
    PROBED.write_text(json.dumps(probed, indent=0, sort_keys=True), encoding="utf-8", newline="\n")
    print(f"added {len(added)}; watching {len(rows)} boards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
