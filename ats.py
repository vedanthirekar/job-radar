"""Fetch open jobs from public ATS job board feeds and normalize them.

Greenhouse, Lever and Ashby all publish free, public JSON feeds of every
open job on a company's board. No login, no scraping of HTML.
"""
from __future__ import annotations

import html
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone

UA = "job-radar/1.0 (personal job alert script)"
TIMEOUT = 20


@dataclass
class Job:
    ats: str
    slug: str
    company: str
    job_id: str
    title: str
    location: str
    url: str
    posted_at: datetime | None = None
    description: str = ""
    is_remote: bool | None = None
    country: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return f"{self.ats}:{self.slug}:{self.job_id}"


class FetchError(Exception):
    pass


def http_get_json(url: str, retries: int = 2):
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise FetchError(f"404 {url}")
            last = e
        except Exception as e:  # network blip, timeout, bad JSON
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise FetchError(f"{url}: {last}")


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = html.unescape(s)          # Greenhouse double-encodes HTML
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def from_ms(ms) -> datetime | None:
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
    except (TypeError, ValueError):
        return None


# ---------------- Greenhouse ----------------
GH_LIST = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
GH_ONE = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{id}"


def parse_greenhouse(slug: str, company: str, data: dict) -> list[Job]:
    jobs = []
    for j in data.get("jobs", []):
        loc = (j.get("location") or {}).get("name", "") or ""
        jobs.append(Job(
            ats="greenhouse", slug=slug,
            company=company or j.get("company_name") or slug,
            job_id=str(j.get("id")),
            title=(j.get("title") or "").strip(),
            location=loc,
            url=j.get("absolute_url") or "",
            posted_at=parse_iso(j.get("first_published")) or parse_iso(j.get("updated_at")),
            description=strip_html(j.get("content", "")),
            is_remote=True if "remote" in loc.lower() else None,
        ))
    return jobs


def greenhouse_description(slug: str, job_id: str) -> str:
    data = http_get_json(GH_ONE.format(slug=slug, id=job_id))
    return strip_html(data.get("content", ""))


# ---------------- Lever ----------------
LEVER_LIST = "https://api.lever.co/v0/postings/{slug}?mode=json"


def parse_lever(slug: str, company: str, data: list) -> list[Job]:
    jobs = []
    for j in data or []:
        cats = j.get("categories") or {}
        loc = cats.get("location") or ", ".join(cats.get("allLocations") or []) or ""
        parts = [j.get("descriptionPlain") or strip_html(j.get("description", ""))]
        for lst in j.get("lists") or []:
            parts.append(lst.get("text", ""))
            parts.append(strip_html(lst.get("content", "")))
        parts.append(j.get("additionalPlain") or strip_html(j.get("additional", "")))
        workplace = (j.get("workplaceType") or "").lower()
        jobs.append(Job(
            ats="lever", slug=slug, company=company or slug,
            job_id=str(j.get("id")),
            title=(j.get("text") or "").strip(),
            location=loc,
            url=j.get("hostedUrl") or j.get("applyUrl") or "",
            posted_at=from_ms(j.get("createdAt")),
            description=" ".join(p for p in parts if p),
            is_remote=True if workplace == "remote" or "remote" in loc.lower() else None,
            country=(j.get("country") or "").upper(),
            extra={"commitment": cats.get("commitment", "")},
        ))
    return jobs


# ---------------- Ashby ----------------
ASHBY_LIST = "https://api.ashbyhq.com/posting-api/job-board/{slug}"


def parse_ashby(slug: str, company: str, data: dict) -> list[Job]:
    jobs = []
    for j in data.get("jobs", []):
        if j.get("isListed") is False:
            continue
        addr = ((j.get("address") or {}).get("postalAddress") or {})
        locs = [j.get("location") or ""]
        for s in j.get("secondaryLocations") or []:
            locs.append(s.get("location") or "")
        jobs.append(Job(
            ats="ashby", slug=slug, company=company or slug,
            job_id=str(j.get("id")),
            title=(j.get("title") or "").strip(),
            location=" / ".join(l for l in locs if l),
            url=j.get("jobUrl") or j.get("applyUrl") or "",
            posted_at=parse_iso(j.get("publishedAt")),
            description=j.get("descriptionPlain") or strip_html(j.get("descriptionHtml", "")),
            is_remote=j.get("isRemote"),
            country=(addr.get("addressCountry") or ""),
            extra={"employmentType": j.get("employmentType", "")},
        ))
    return jobs


def fetch_board(ats: str, slug: str, company: str = "") -> list[Job]:
    if ats == "greenhouse":
        return parse_greenhouse(slug, company, http_get_json(GH_LIST.format(slug=slug)))
    if ats == "lever":
        return parse_lever(slug, company, http_get_json(LEVER_LIST.format(slug=slug)))
    if ats == "ashby":
        return parse_ashby(slug, company, http_get_json(ASHBY_LIST.format(slug=slug)))
    raise ValueError(f"unknown ats {ats}")


def probe_url(ats: str, slug: str) -> str:
    return {"greenhouse": GH_LIST, "lever": LEVER_LIST, "ashby": ASHBY_LIST}[ats].format(slug=slug)
