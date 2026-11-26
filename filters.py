"""Decide which jobs are worth a phone alert.

Order: title -> seniority -> location -> description (sponsorship, citizenship).
Every drop records a reason so the log can show why a job was skipped.
"""
from __future__ import annotations

import re

from ats import Job

# A title must name a technical role...
ROLE = re.compile(
    r"\b(engineer(ing)?|developer|scientist|swe|sde|programmer|builder|"
    r"researcher|data analyst|analytics|machine learning|ml|ai|llm|genai|fde|"
    r"member of technical staff|mts)\b", re.I)

# ...in one of Vedant's tracks.
TRACK = re.compile(
    r"\b(software|swe|sde|back[- ]?end|full[- ]?stack|front[- ]?end|web|platform|"
    r"product engineer|applications? (developer|engineer)|"
    r"ai|a\.i\.|ml|machine learning|deep learning|llm|genai|gen ai|generative|agent(s|ic)?|nlp|"
    r"data|analytics|bi\b|business intelligence|"
    r"forward[- ]deployed|fde|deployment|solutions? engineer|implementation engineer|"
    r"automation|integration|applied|research engineer|mlops|infrastructure|devops|cloud|python)\b", re.I)

# Titles that match the words above but are not his kind of job.
NOT_TRACK = re.compile(
    r"\b(sales|account (executive|manager)|marketing|recruit(er|ing)|talent|"
    r"mechanical|electrical|hardware|civil|chemical|structural|manufacturing|"
    r"process engineer|quality engineer|test technician|technician|field service|"
    r"rf|analog|asic|fpga|silicon|verification engineer|firmware|"
    r"customer success|support engineer|technical support|help ?desk|it support|"
    r"legal|counsel|paralegal|accountant|finance manager|nurse|"
    r"designer|copywriter|writer|content)\b", re.I)

SENIOR = re.compile(
    r"\b(senior|sr\.?|staff|principal|lead|leader|manager|management|director|head|vp|"
    r"vice president|chief|cto|architect|distinguished|fellow|expert|"
    r"iii|iv|v\b|level (3|4|5)|l[4-9]\b|e[5-9]\b)\b", re.I)

# Places that are clearly outside the US.
NON_US = re.compile(
    r"\b(uk|united kingdom|england|london|manchester|edinburgh|ireland|dublin|"
    r"canada|toronto|vancouver|montreal|ottawa|calgary|"
    r"india|bengaluru|bangalore|hyderabad|pune|mumbai|delhi|gurgaon|gurugram|noida|chennai|"
    r"germany|berlin|munich|france|paris|spain|madrid|barcelona|portugal|lisbon|"
    r"netherlands|amsterdam|poland|warsaw|krakow|romania|ukraine|serbia|"
    r"sweden|stockholm|denmark|copenhagen|norway|finland|switzerland|zurich|austria|vienna|"
    r"italy|milan|belgium|czech|prague|hungary|budapest|greece|israel|tel aviv|"
    r"singapore|japan|tokyo|korea|seoul|china|beijing|shanghai|hong kong|taiwan|"
    r"philippines|manila|vietnam|indonesia|malaysia|thailand|australia|sydney|melbourne|"
    r"new zealand|mexico|brazil|sao paulo|argentina|buenos aires|colombia|bogota|chile|"
    r"costa rica|peru|uruguay|nigeria|kenya|south africa|egypt|uae|dubai|saudi|pakistan|"
    r"emea|apac|latam|europe|asia)\b", re.I)

US_HINT = re.compile(
    r"\b(us|usa|u\.s\.|united states|remote|anywhere|"
    r"al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|mt|ne|nv|nh|nj|nm|"
    r"ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy|dc)\b", re.I)

# Hard stops in the job description: these employers won't take an OPT candidate.
NO_SPONSOR = [
    r"(not|unable to|cannot|can['’]?t|won['’]?t|will not|do not|does not|is not able to|are not able to)\s+"
    r"(currently\s+)?(be\s+)?(able to\s+)?(offer|provide|sponsor|support|consider)[^.]{0,60}(sponsor|visa|h-?1b|work authori[sz]ation)",
    r"without\s+(the\s+)?(need\s+for\s+|requiring\s+)?(current\s+or\s+future\s+|now\s+or\s+in\s+the\s+future\s+)?"
    r"(employer\s+|visa\s+|company\s+)?sponsorship",
    r"\bno\s+(visa\s+|h-?1b\s+)?sponsorship",
    r"sponsorship\s+(is\s+|will\s+)?(not\s+|un)(be\s+)?(available|offered|provided|possible|supported)",
    r"not\s+(eligible|open)\s+(for|to)\s+(visa\s+)?sponsorship",
    r"(must|required to|need to)\s+be\s+(legally\s+)?authori[sz]ed\s+to\s+work[^.]{0,80}without[^.]{0,30}sponsor",
    r"(must|required to)\s+be\s+(a\s+)?(u\.?s\.?|united states)\s+(citizen|person)",
    r"(u\.?s\.?|united states)\s+citizenship\s+(is\s+)?(required|mandatory)",
    r"\b(us|u\.s\.)\s+citizens?\s+only",
    r"(active|current|secret|top secret|ts/sci|ts sci)\s+(security\s+)?clearance",
    r"(ability|able|eligible)\s+to\s+(obtain|get|maintain)\s+(a\s+)?(security\s+)?clearance",
    r"\bitar\b",
    r"green card holders?\s+(only|or u\.?s\.? citizens)",
    r"citizens?\s+or\s+(lawful\s+)?permanent\s+residents?\s+only",
    r"\b(does|do|will)\s+not\s+sponsor\b",
    r"(unable to|cannot|can['’]?t|not able to|won['’]?t|will not|do not|does not|don['’]?t)\s+(currently\s+)?sponsor",
    r"\bopt\b[^.]{0,40}\bnot\s+(eligible|accepted|considered)",
]
NO_SPONSOR_RE = [re.compile(p, re.I) for p in NO_SPONSOR]

YEARS_RE = re.compile(
    r"(\d{1,2})\s*\+?\s*(?:-|–|to)?\s*(?:\d{1,2})?\s*\+?\s*years?(?:\s+of)?[^.]{0,60}?(experience|industry|professional)",
    re.I)

INTERN_RE = re.compile(r"\b(intern|internship|co-?op)\b", re.I)


def title_ok(title: str) -> tuple[bool, str]:
    mts = re.search(r"member of (the )?technical staff", title, re.I)
    if mts:
        title = re.sub(r"member of (the )?technical staff", "software engineer", title, flags=re.I)
    if not ROLE.search(title):
        return False, "title: not a technical role"
    if not TRACK.search(title):
        return False, "title: outside tracks"
    if NOT_TRACK.search(title):
        return False, "title: excluded kind of role"
    if SENIOR.search(title):
        return False, "title: too senior"

    return True, ""


US_STATE_CODE = re.compile(
    r"(?:,|\(|\s-)\s*(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|"
    r"NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\b")
US_WORDS = re.compile(
    r"\b(usa|u\.s\.a?\.?|united states|us[- ]remote|remote[- ,(]*us\b|\bus\b|americas|north america|"
    r"alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|florida|hawaii|idaho|illinois|"
    r"indiana|iowa|kansas|kentucky|louisiana|maine|maryland|massachusetts|michigan|minnesota|mississippi|"
    r"missouri|montana|nebraska|nevada|new hampshire|new jersey|new mexico|new york|north carolina|"
    r"north dakota|ohio|oklahoma|oregon|pennsylvania|rhode island|south carolina|south dakota|tennessee|"
    r"texas|utah|vermont|virginia|washington|wisconsin|wyoming|"
    r"san francisco|bay area|seattle|boston|chicago|austin|denver|atlanta|los angeles|nyc|brooklyn|"
    r"palo alto|mountain view|menlo park|sunnyvale|san jose|san mateo|redwood city|oakland|berkeley|"
    r"san diego|irvine|santa monica|portland|salt lake|phoenix|dallas|houston|miami|philadelphia|"
    r"pittsburgh|detroit|minneapolis|nashville|raleigh|durham|charlotte|indianapolis|columbus|"
    r"cincinnati|cleveland|st\.? louis|kansas city|madison|ann arbor|boulder|cambridge, ma|arlington)\b", re.I)


def location_ok(job: Job) -> tuple[bool, str]:
    loc = job.location or ""
    country = (job.country or "").strip().lower()
    us_country = country in ("us", "usa", "united states", "united states of america")
    codes = US_STATE_CODE.findall(loc)
    strong_us = us_country or bool(US_WORDS.search(loc)) or any(c != "IN" for c in codes)
    non_us = bool(NON_US.search(loc)) or (country and not us_country)
    if strong_us:
        return True, ""
    if codes and not non_us:          # only ", IN" and nothing foreign: Indiana
        return True, ""
    if non_us:
        return False, f"location: {(loc or job.country)[:60]}"
    return True, ""                   # "Remote", "Hybrid", blank: keep


def description_block(desc: str) -> str:
    """Return the matching phrase if the description rules him out, else ''."""
    if not desc:
        return ""
    for rx in NO_SPONSOR_RE:
        m = rx.search(desc)
        if m:
            return m.group(0)[:90]
    return ""


def min_years(desc: str) -> int | None:
    found = []
    for m in YEARS_RE.finditer(desc or ""):
        n = int(m.group(1))
        if 1 <= n <= 15:
            found.append(n)
    return min(found) if found else None


SPONSOR_YES = re.compile(
    r"(visa sponsorship (is\s+)?(available|offered|provided)|sponsorship (is\s+)?(available|offered|provided)|"
    r"we (do\s+|can\s+|will\s+)?sponsor|willing to sponsor|h-?1b (sponsorship|transfer)s? (available|welcome|supported)|"
    r"f-?1 (students?|visa)|\b(stem )?opt\b(?![- ]?(in|out))|\bcpt\b)", re.I)


def flags_for(job: Job) -> list[str]:
    flags = []
    if SPONSOR_YES.search(job.description or ""):
        flags.append("mentions sponsorship/OPT")
    yrs = min_years(job.description)
    if yrs is not None and yrs >= 3:
        flags.append(f"{yrs}+ yrs asked")
    if INTERN_RE.search(job.title):
        flags.append("internship")
    return flags


# ---------------- resume picker ----------------
RESUMES = {
    "AI Engineer resume": [
        r"\bai\b", r"\bllm", r"genai|generative", r"agent", r"\brag\b", r"langchain|langgraph",
        r"prompt", r"forward[- ]deployed|\bfde\b", r"applied ai", r"evaluation|evals?\b", r"nlp",
        r"openai|anthropic|claude", r"vector",
    ],
    "SWE resume": [
        r"software engineer|\bswe\b|\bsde\b", r"back[- ]?end", r"full[- ]?stack", r"front[- ]?end",
        r"\breact\b", r"typescript|javascript|node", r"\bapi", r"web app|web application",
        r"microservice", r"\bjava\b|\bgo\b|golang", r"platform", r"fastapi|flask|django",
    ],
    "Data/ML resume": [
        r"data scien", r"machine learning|\bml\b", r"data engineer", r"analytic", r"data analyst",
        r"spark|airflow|dbt|etl", r"statistic", r"forecast", r"pytorch|scikit|xgboost",
        r"tableau|power bi", r"experiment|a/b",
    ],
}
RESUME_RE = {k: [re.compile(p, re.I) for p in v] for k, v in RESUMES.items()}


def pick_resume(job: Job) -> str:
    scores = {}
    for name, pats in RESUME_RE.items():
        s = 0
        for rx in pats:
            if rx.search(job.title):
                s += 4
            s += min(len(rx.findall(job.description or "")), 3)
        scores[name] = s
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "SWE resume"
