# Founder outreach

Cold outreach to small companies (roughly under 500 people, ideally under 200) that have filed H-1Bs for tech roles in 2025 or 2026, whether or not they have a job posted.

Everything about this lives in this folder, not in any chat. Any new chat can pick up from here.

## Files

| File | What it is |
| --- | --- |
| `targets.csv` | Every candidate company. `status` is blank (not started), `researched`, `skipped`, `drafted`, `sent`, `replied`, `interview`, `no` |
| `companies/<slug>.md` | One file per company: what they do, the specific hook, people to contact, the email and LinkedIn drafts, and a log of what happened |
| `batches/<date>.md` | Each night's research batch: the list of companies ready for emails the next morning |

## Daily flow

1. **Night (automatic):** a scheduled task researches the next 20 companies, writes their files and a batch file, and marks them `researched`.
2. **Morning (Vedant, 1 message):** open a new chat and say "enrich today's founder batch". Claude confirms the Apollo credit cost once, gets work emails (1 credit per person), puts every email in Gmail as a draft, and marks the companies `drafted`.
3. **Vedant:** reads each draft, sends it (or schedules it for 8 to 9 am in the recipient's time zone), sends the LinkedIn notes, and says "sent" so status becomes `sent`.
4. **Replies:** the twice-daily inbox check flags replies. Update the company file's log and `targets.csv`.

## Writing rules

- Open with one specific, real thing about the company or person (a launch, a post, a product decision). Nothing generic.
- One relevant piece of Vedant's work, in plain words. No achievement lists, no boasting, no sales pitch.
- Present Project 990 as his job: "AI Engineer at Project 990".
- One ask: a 15-minute chat, or the right person to talk to. Engineers get a referral ask.
- Close with: "I'm on STEM OPT, so no visa sponsorship is needed for up to three years."
- About 90 to 120 words. No em dashes. LinkedIn notes up to 300 characters.
- Never send anything. Drafts only.
