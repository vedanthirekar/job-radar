"""Write docs/index.html: a page of recent alerts with Apply buttons, served by GitHub Pages."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
LOG = ROOT / "data" / "jobs_log.csv"
OUT = ROOT / "docs" / "index.html"
DAYS = 7

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="180">
<title>Job radar</title>
<style>
  :root { --bg:#fafaf9; --fg:#1c1917; --muted:#78716c; --line:#e7e5e4; --accent:#15803d; --chip:#f5f5f4; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#1c1917; --fg:#f5f5f4; --muted:#a8a29e; --line:#3f3a36; --accent:#4ade80; --chip:#292524; }
  }
  * { box-sizing: border-box; }
  body { margin:0; font:15px/1.45 system-ui, -apple-system, Segoe UI, sans-serif; background:var(--bg); color:var(--fg); }
  header { position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line); padding:14px 20px;
           display:flex; gap:16px; align-items:center; flex-wrap:wrap; }
  h1 { font-size:18px; margin:0; }
  .meta { color:var(--muted); font-size:13px; }
  .controls { margin-left:auto; display:flex; gap:8px; flex-wrap:wrap; }
  button.f { border:1px solid var(--line); background:var(--chip); color:var(--fg); border-radius:999px;
             padding:4px 12px; font-size:13px; cursor:pointer; }
  button.f.on { border-color:var(--accent); color:var(--accent); }
  main { max-width:1000px; margin:0 auto; padding:8px 20px 40px; }
  .job { display:grid; grid-template-columns: 1fr auto; gap:4px 16px; padding:14px 0; border-bottom:1px solid var(--line); }
  .job.applied { opacity:.45; }
  .title { font-weight:600; }
  .co { color:var(--muted); font-weight:500; }
  .sub { color:var(--muted); font-size:13px; grid-column:1; }
  .tags { grid-column:1; display:flex; gap:6px; flex-wrap:wrap; }
  .tag { background:var(--chip); border-radius:6px; padding:1px 8px; font-size:12px; }
  .tag.good { color:var(--accent); }
  .act { grid-row:1 / span 3; grid-column:2; display:flex; flex-direction:column; gap:6px; align-items:flex-end; }
  a.apply { background:var(--accent); color:#fff; text-decoration:none; padding:6px 14px; border-radius:8px; font-weight:600; }
  @media (prefers-color-scheme: dark) { a.apply { color:#052e16; } }
  label { font-size:13px; color:var(--muted); cursor:pointer; }
  .new { color:var(--accent); font-weight:600; }
  .empty { color:var(--muted); padding:40px 0; text-align:center; }
</style>
</head>
<body>
<header>
  <h1>Job radar</h1>
  <span class="meta" id="meta"></span>
  <div class="controls" id="controls"></div>
</header>
<main id="list"></main>
<script>
const JOBS = __DATA__;
const UPDATED = "__UPDATED__";
let store = {};
try { store = JSON.parse(localStorage.getItem("applied") || "{}"); } catch (e) {}
const save = () => { try { localStorage.setItem("applied", JSON.stringify(store)); } catch (e) {} };
let filter = "All", hideApplied = false;

function ago(iso) {
  if (!iso) return "";
  const m = Math.round((Date.now() - new Date(iso)) / 60000);
  if (m < 60) return m + " min ago";
  if (m < 1440) return Math.round(m / 60) + " h ago";
  return Math.round(m / 1440) + " d ago";
}
function esc(s) { return String(s || "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

function render() {
  const resumes = ["All", ...new Set(JOBS.map(j => j.resume).filter(Boolean))];
  document.getElementById("controls").innerHTML =
    resumes.map(r => `<button class="f ${r === filter ? "on" : ""}" data-r="${esc(r)}">${esc(r)}</button>`).join("") +
    `<button class="f ${hideApplied ? "on" : ""}" id="hide">Hide applied</button>`;
  document.querySelectorAll("button[data-r]").forEach(b => b.onclick = () => { filter = b.dataset.r; render(); });
  document.getElementById("hide").onclick = () => { hideApplied = !hideApplied; render(); };

  const rows = JOBS.filter(j => (filter === "All" || j.resume === filter) && !(hideApplied && store[j.url]));
  document.getElementById("meta").textContent =
    `${JOBS.length} alerts in the last 7 days · updated ${ago(UPDATED)} · refreshes every 3 min`;
  const list = document.getElementById("list");
  if (!rows.length) { list.innerHTML = '<div class="empty">Nothing here yet.</div>'; return; }
  list.innerHTML = rows.map(j => {
    const t = j.posted_at || j.checked_at;
    const fresh = t && (Date.now() - new Date(t)) < 3600000;
    const tags = [];
    if (j.sponsor) tags.push(`<span class="tag ${j.sponsor.startsWith("Sponsors") ? "good" : ""}">${esc(j.sponsor)}</span>`);
    (j.flags || "").split("; ").filter(Boolean).forEach(f =>
      tags.push(`<span class="tag ${f.includes("sponsorship") ? "good" : ""}">${esc(f)}</span>`));
    return `<div class="job ${store[j.url] ? "applied" : ""}">
      <div><span class="title">${esc(j.title)}</span> <span class="co">· ${esc(j.company)}</span></div>
      <div class="sub">${esc(j.location || "Location not listed")} · ${fresh ? '<span class="new">' : ""}posted ${ago(t)}${fresh ? "</span>" : ""} · ${esc(j.resume)}</div>
      <div class="tags">${tags.join("")}</div>
      <div class="act">
        <a class="apply" href="${esc(j.url)}" target="_blank" rel="noopener">Apply</a>
        <label><input type="checkbox" data-u="${esc(j.url)}" ${store[j.url] ? "checked" : ""}> Applied</label>
      </div></div>`;
  }).join("");
  document.querySelectorAll("input[data-u]").forEach(c => c.onchange = () => {
    if (c.checked) store[c.dataset.u] = Date.now(); else delete store[c.dataset.u];
    save(); render();
  });
}
render();
</script>
</body>
</html>
"""


def build() -> int:
    rows = []
    if LOG.exists():
        cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
        with LOG.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("alerted") != "yes":
                    continue
                try:
                    when = datetime.fromisoformat(r["checked_at"])
                except (KeyError, ValueError):
                    continue
                if when >= cutoff:
                    rows.append({k: r.get(k, "") for k in
                                 ("checked_at", "company", "title", "location", "url", "posted_at",
                                  "resume", "flags", "sponsor")})
    seen, uniq = set(), []
    for r in sorted(rows, key=lambda r: r["posted_at"] or r["checked_at"], reverse=True):
        if r["url"] not in seen:
            seen.add(r["url"])
            uniq.append(r)
    data = json.dumps(uniq, ensure_ascii=False).replace("</", "<\\/")
    html = PAGE.replace("__DATA__", data).replace(
        "__UPDATED__", datetime.now(timezone.utc).isoformat(timespec="minutes"))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    return len(uniq)


if __name__ == "__main__":
    print(f"dashboard: {build()} jobs")
