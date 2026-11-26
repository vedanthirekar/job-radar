# job-radar

Pings my phone within about 10 to 20 minutes of a matching job going up on a company's own careers page.

It reads the public job feeds that Greenhouse, Lever and Ashby publish for every company that uses them. No LinkedIn, no Indeed, no scraping of web pages.

## What runs

| Workflow | When | What it does |
| --- | --- | --- |
| Job radar | every 10 min | Checks every board in `companies.csv`, alerts on new matching jobs |
| Find company job boards | when `candidates.txt` changes, and Mondays | Figures out which system each company uses and adds it to `companies.csv` |
| Sponsor data | when `sponsors.py` changes, and monthly | Builds `data/sponsors.csv` from DOL H-1B filings and adds sponsoring companies to the watch list |

Everything runs on GitHub's servers. Your laptop can be off.

## What gets an alert

Only jobs that pass all of these:

- **Title** is an AI, ML, data, software, FDE or applied AI role, including internships
- **Not senior**: senior, staff, principal, lead, manager, director, III and up are skipped
- **US** location, or remote with no non-US country
- **Fresh**: posted in the last 72 hours (stops old reposts)
- **No sponsorship or citizenship blockers** in the description ("without sponsorship now or in the future", "US citizen", "clearance", "ITAR" and similar)

Each alert shows the location, minutes since posting, which resume to use, the company's H-1B record, and notes like "3+ yrs asked" or "mentions sponsorship/OPT". Tapping it opens the apply page.

New boards are learned quietly on their first check, so adding a company never floods your phone with its old jobs.

## Setup

1. Repo Settings, then Secrets and variables, then Actions, then New repository secret: `NTFY_TOPIC` = your private ntfy channel name.
2. Actions tab: enable workflows if GitHub asks.
3. Actions, then Job radar, then Run workflow, with "Send one test alert" ticked. Your phone should buzz.

If alerts stop with a 429 error in the logs, make a free account on ntfy.sh, create an access token, and save it as a second secret, `NTFY_TOKEN`.

## Everyday use

- **Add a company:** add its name to `candidates.txt` and commit. To force a board: `Acme | greenhouse:acme`.
- **Why didn't X alert me?** Open `data/jobs_log.csv`. Every matching-title job is logged with `alerted` and the `reason`.
- **Change filters:** edit `filters.py`. Run `python -m pytest -q` after changes.
- **Test locally:** `DRY_RUN=1 python radar.py` prints alerts instead of sending them.

## If the sponsor download fails

dol.gov sometimes blocks automated downloads. Download the `LCA_Disclosure_Data_FY2026_Q*.xlsx` files from the DOL OFLC performance data page, put them in `data/dol/` on your machine, run `pip install python-calamine && python sponsors.py && python detect.py`, and commit `data/sponsors.csv`, `data/sponsor_candidates.txt`, `companies.csv` and `data/probed.json`. Don't commit the xlsx files; they are too big for git.
