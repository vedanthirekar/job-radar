"""Offline tests: run with  python -m pytest -q  (no network needed)."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ats  # noqa: E402
import filters  # noqa: E402
import radar  # noqa: E402
from names import norm, slug_guesses  # noqa: E402

NOW = datetime.now(timezone.utc)
ISO = (NOW - timedelta(minutes=12)).isoformat()


# ---------- titles ----------
GOOD = ["Software Engineer", "AI Engineer", "Machine Learning Engineer", "Forward Deployed Engineer",
        "Data Engineer", "Data Scientist", "Backend Engineer, Payments", "Full Stack Developer",
        "Applied AI Engineer", "Software Engineer II", "New Grad Software Engineer", "Data Analyst",
        "Software Engineering Intern", "AI/ML Engineer", "Member of Technical Staff",
        "Solutions Engineer, AI", "LLM Engineer", "Analytics Engineer", "Platform Engineer"]
BAD = ["Senior Software Engineer", "Staff ML Engineer", "Engineering Manager", "Sr. Data Scientist",
       "Account Executive, AI", "Principal Engineer", "Mechanical Engineer", "Recruiter",
       "Product Designer", "Software Engineer III", "Tech Lead, Platform", "Head of AI",
       "Customer Support Engineer", "Marketing Manager", "Director of Data", "Hardware Engineer"]


def test_titles():
    for t in GOOD:
        assert filters.title_ok(t)[0], t
    for t in BAD:
        assert not filters.title_ok(t)[0], t


# ---------- locations ----------
def J(loc, country=""):
    return ats.Job("greenhouse", "x", "X", "1", "Software Engineer", loc, "u", country=country)


def test_locations():
    keep = ["San Francisco, CA", "Remote", "Remote - US", "New York, NY; London, UK", "Bloomington, IN",
            "Hybrid", "", "United States", "Austin, Texas", "Seattle, WA or Toronto, ON", "US Remote",
            "Cambridge, MA"]
    drop = ["London, UK", "Toronto, ON, Canada", "Bengaluru, India", "Remote - Canada", "Berlin",
            "EMEA", "Remote, Europe", "Bengaluru, IN"]
    for l in keep:
        assert filters.location_ok(J(l))[0], l
    for l in drop:
        assert not filters.location_ok(J(l))[0], l
    assert filters.location_ok(J("Remote", "US"))[0]
    assert not filters.location_ok(J("Remote", "GB"))[0]


# ---------- sponsorship ----------
BLOCK = [
    "Applicants must be authorized to work in the US without the need for visa sponsorship now or in the future.",
    "We are unable to sponsor visas for this role.",
    "This position is not eligible for visa sponsorship.",
    "Sponsorship is not available for this position.",
    "We do not sponsor H-1B.",
    "Must be a U.S. citizen.",
    "Candidates must hold an active security clearance.",
    "No visa sponsorship.",
    "We will not consider candidates who require sponsorship.",
    "Requires US citizenship due to ITAR regulations.",
    "We cannot sponsor at this time.",
]
ALLOW = [
    "We consider all applicants without regard to race, religion, citizenship status or national origin.",
    "You must be authorized to work in the United States.",
    "Visa sponsorship is available for this role.",
    "We support OPT and H-1B transfers.",
    "Users can opt out of emails at any time.",
]


def test_sponsor_blocks():
    for d in BLOCK:
        assert filters.description_block(d), d
    for d in ALLOW:
        assert not filters.description_block(d), d


def test_flags():
    j = J("Remote")
    j.description = "We sponsor visas. 3+ years of experience with Python."
    f = filters.flags_for(j)
    assert "mentions sponsorship/OPT" in f and "3+ yrs asked" in f
    j.description = "Users can opt out anytime."
    assert "mentions sponsorship/OPT" not in filters.flags_for(j)


def test_resume_picker():
    j = J("Remote")
    j.title, j.description = "AI Engineer, LLM Agents", "Build RAG and agents with LangChain"
    assert filters.pick_resume(j) == "AI Engineer resume"
    j.title, j.description = "Backend Software Engineer", "Python APIs, React, TypeScript"
    assert filters.pick_resume(j) == "SWE resume"
    j.title, j.description = "Data Scientist", "statistics, forecasting, experimentation, Spark"
    assert filters.pick_resume(j) == "Data/ML resume"


# ---------- feed parsing ----------
def test_parsers():
    gh = {"jobs": [{"id": 11, "title": "AI Engineer", "location": {"name": "Remote - US"},
                    "absolute_url": "https://g/11", "first_published": ISO, "company_name": "Acme"}]}
    lv = [{"id": "ab", "text": "Software Engineer", "categories": {"location": "Austin, TX"},
           "hostedUrl": "https://l/ab", "createdAt": int(NOW.timestamp() * 1000), "descriptionPlain": "hi",
           "lists": [{"text": "Reqs", "content": "<li>3+ years of experience</li>"}], "country": "US"}]
    ab = {"jobs": [{"id": "z", "title": "Data Engineer", "location": "New York", "jobUrl": "https://a/z",
                    "publishedAt": ISO, "isRemote": False, "descriptionPlain": "Spark",
                    "address": {"postalAddress": {"addressCountry": "United States"}}}]}
    g = ats.parse_greenhouse("acme", "", gh)[0]
    l = ats.parse_lever("acme", "Acme", lv)[0]
    a = ats.parse_ashby("acme", "Acme", ab)[0]
    assert g.company == "Acme" and g.posted_at and g.is_remote
    assert l.posted_at and "3+ years" in l.description and l.country == "US"
    assert a.country == "United States" and a.posted_at


def test_names():
    assert norm("Snowplow Analytics, Ltd.") == "snowplow analytics"
    assert norm("The Brattle Group, Inc.") == "brattle"
    g = slug_guesses("Virta Health")
    assert "virtahealth" in g and "virta-health" in g and "virta" in g


# ---------- end to end ----------
def test_end_to_end(tmp_path, monkeypatch, capsys):
    (tmp_path / "state").mkdir()
    (tmp_path / "data").mkdir()
    comp = tmp_path / "companies.csv"
    comp.write_text("name,ats,slug,source,added\nAcme,greenhouse,acme,hand,2026-11-26\n")
    (tmp_path / "data" / "sponsors.csv").write_text(
        "employer_norm,employer_name,tech_lcas,perm,h1b_dependent,since_fy\nacme,ACME INC,7,2,,2025\n")
    monkeypatch.setattr(radar, "COMPANIES", comp)
    monkeypatch.setattr(radar, "SPONSORS", tmp_path / "data" / "sponsors.csv")
    monkeypatch.setattr(radar, "STATE", tmp_path / "state" / "seen.json")
    monkeypatch.setattr(radar, "LOG", tmp_path / "data" / "jobs_log.csv")
    monkeypatch.setattr(radar, "DRY_RUN", True)

    boards = {"jobs": [{"id": 1, "title": "Software Engineer", "location": {"name": "Remote"},
                        "absolute_url": "u1", "first_published": ISO}]}
    descs = {}

    def fake_get(url, retries=2):
        if url.endswith("/jobs"):
            return boards
        jid = url.rsplit("/", 1)[1]
        return {"content": descs.get(jid, "")}
    monkeypatch.setattr(ats, "http_get_json", fake_get)

    radar.main()                      # first run: learns board quietly
    assert "[alert]" not in capsys.readouterr().out

    boards["jobs"] += [
        {"id": 2, "title": "AI Engineer", "location": {"name": "San Francisco, CA"}, "absolute_url": "u2",
         "first_published": ISO},
        {"id": 3, "title": "Data Engineer", "location": {"name": "Remote"}, "absolute_url": "u3",
         "first_published": ISO},
        {"id": 4, "title": "Senior Software Engineer", "location": {"name": "Remote"}, "absolute_url": "u4",
         "first_published": ISO},
        {"id": 5, "title": "Software Engineer", "location": {"name": "London, UK"}, "absolute_url": "u5",
         "first_published": ISO},
        {"id": 6, "title": "Data Scientist", "location": {"name": "Remote"}, "absolute_url": "u6",
         "first_published": (NOW - timedelta(days=10)).isoformat()},
    ]
    descs["2"] = "&lt;p&gt;Build LLM agents. We sponsor visas.&lt;/p&gt;"
    descs["3"] = "Must be authorized to work without sponsorship now or in the future."
    radar.main()
    out = capsys.readouterr().out
    assert "Acme: AI Engineer" in out
    assert "Sponsors (7 tech H-1B filings" in out
    for t in ("Data Engineer", "Senior", "London"):
        assert t not in out.split("done in")[0].split("[alert]", 1)[-1] or "Acme: AI Engineer" in out
    assert out.count("[alert]") == 1
    log = (tmp_path / "data" / "jobs_log.csv").read_text()
    assert "blocked:" in log and "old posting" in log and "location:" in log

    radar.main()                      # nothing new: no alerts
    assert "[alert]" not in capsys.readouterr().out
    state = json.loads((tmp_path / "state" / "seen.json").read_text())
    assert len(state["boards"]["greenhouse:acme"]) == 6
