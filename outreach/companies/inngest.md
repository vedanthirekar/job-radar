# Inngest
- Site: inngest.com · Remote-first, SF office · size ~27 on About page · 1 tech H-1B filings
- What they do: A durable execution platform for background jobs, queues and AI agent workflows, with retries, concurrency control and observability.
- Hook: "Sandboxes: isolated microVMs from any function" (Oct 6, 2026): step.sandbox.create starts a microVM in under a second, and every create, command and destroy call is a durable step on the run trace. Newer: webhook failure grouping (Nov 23, 2026, https://www.inngest.com/changelog/2026-11-23-webhook-recent-activity).
- Hook source: https://www.inngest.com/changelog/2026-10-06-sandboxes
- Vedant's angle: Multi-agent ticket resolution system: LangGraph, FastAPI, PostgreSQL job queue, human approval step.

## People
- Dan Farrelly, CTO & Founder · LinkedIn: not found · source: https://inngest.com/about (email: pending Apollo)
- Duc Nguyen, Engineering Manager · LinkedIn: not found · source: https://inngest.com/about (email: pending Apollo)
- Notes: CEO: Tony Holdstock-Brown.

## Email draft
To: Dan Farrelly
Subject: Sandboxes as durable steps

Hi Dan,

The Sandboxes changelog had a neat design choice: every create, command, and destroy call is a durable step on the run trace. That's what I wanted last year and ended up building a rougher version of myself.

In a side project I built a multi-agent ticket resolution system with LangGraph and FastAPI, using a PostgreSQL job queue for retries and a human approval step before sensitive actions. Getting the queue right was most of the work. Today I'm an AI Engineer at Project 990, running an LLM pipeline on a GPU cluster.

Would you be open to a 15-minute chat about engineering at Inngest?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Dan Farrelly (216 chars): Hi Dan, making every sandbox call a durable step is a great choice. I built a multi-agent ticket system on a Postgres job queue with human approval steps, and I'm an AI Engineer at Project 990. Would love to connect.
- Duc Nguyen (222 chars): Hi Duc, I've been following the Inngest changelog, Sandboxes especially. I built an agent system on a Postgres job queue and work as an AI Engineer at Project 990. Open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-26 researched
