# Render
- Site: render.com · San Francisco, CA · size 234 employees (TipRanks, Nov 2026) · 6 tech H-1B filings
- What they do: A cloud platform for deploying web services, databases, workflows, and now isolated sandboxes for AI agents.
- Hook: "Introducing Render Sandboxes: A computer for every agent" (Nov 4, 2026): each sandbox is its own Firecracker microVM, ready in under a second, snapshotted and suspended after 15 idle minutes, with per-sandbox network policy and credential brokering (early access) that keeps API keys out of the sandbox entirely.
- Hook source: https://render.com/blog/introducing-render-sandboxes
- Vedant's angle: Multi-agent ticket resolution side project where agents act freely but sensitive actions wait for human approval, the same "where does the trust boundary sit" question as credential brokering.

## People
- Anurag Goel, Founder & CEO (technical founder; no CTO found) · LinkedIn: not found · source: https://www.cbinsights.com/company/render-1/people (email: pending Apollo)
- Yaroslav Borets, Engineer (co-author of the Sandboxes launch post; title not stated on page) · LinkedIn: not found · source: https://render.com/blog/introducing-render-sandboxes (email: pending Apollo)
- Notes: Company is over 50 people and no CTO was found, so the email goes to the founder. Other Sandboxes authors: Ammar Aijazi, Azzam Aijazi. Mac McCarthy wrote "How Render Workflows powers our internal data pipeline" (Aug 25, 2026), a possible backup contact.

## Email draft
To: Anurag Goel
Subject: Credential brokering in Render Sandboxes

Hi Anurag,

In the Render Sandboxes launch, the detail I kept coming back to was credential brokering: the agent gets its own Firecracker microVM where it can do almost anything, but the API keys never enter it.

I'm an AI Engineer at Project 990, building LLM pipelines. On the side I built a multi-agent ticket resolution system with LangGraph and FastAPI, where agents act on their own but any sensitive action stops and waits for a human to approve it. Deciding where that boundary sits was the hardest design call.

Would you be open to a 15-minute chat about engineering roles at Render?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Anurag Goel (218 chars): Hi Anurag, keeping API keys out of the sandbox entirely with credential brokering is a smart line to draw for agents. I built a multi-agent system where sensitive actions wait for human approval. Would love to connect.
- Yaroslav Borets (245 chars): Hi Yaroslav, enjoyed the Render Sandboxes launch post, especially runtime snapshots and per-sandbox network policy. I'm an AI Engineer at Project 990 building LLM pipelines. Would you be open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-27 researched
