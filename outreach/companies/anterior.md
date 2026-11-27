# Anterior
- Site: anterior.com · New York, NY · size ~31 (Built In NYC) · 4 tech H-1B filings
- What they do: Clinical AI for health plans that automates prior authorization and claims review; it recommends approval or routes to a clinician and never denies care.
- Hook: Partnership with Stellarus (Blue Shield of California spinout) for real-time AI prior authorization (Jul 23, 2026). Anterior's AI can recommend approval or route for review but cannot deny care. Engineer-facing alt: Saul Howard's AI Engineer World's Fair 2026 talk on append-only event logs and replay-based evals (https://ai.engineer/talks/mav15aW9lLM-why-your-enterprise-tech-stack-isnt-ready).
- Hook source: https://anterior.com/insights/anterior-partners-with-stellarus-to-allow-health-plans-to-deliver-real-time-ai-driven-prior-authorization
- Vedant's angle: Multi-agent ticket system where sensitive actions wait for human approval, with a 60-case golden test set; Project 990 LLM-as-judge.

## People
- Abdel Mahmoud, Co-founder & CEO · LinkedIn: https://www.linkedin.com/in/abdelmahmoud/ · source: https://hitconsultant.net/2026/02/12/anterior-raises-40m-clinician-led-ai-health-plans/ (email: pending Apollo)
- Saul Howard, VP of Engineering · LinkedIn: https://linkedin.com/in/saulhoward · source: https://ai.engineer/talks/mav15aW9lLM-why-your-enterprise-tech-stack-isnt-ready (email: pending Apollo)
- Notes: Co-founder Zahid Mahmood (title not stated). No CTO found.

## Email draft
To: Abdel Mahmoud
Subject: Approve or route, never deny

Hi Abdel,

The Stellarus announcement repeated a rule I respect: Anterior's AI can recommend approval or route a case to a clinician, but never denies care. I made a similar choice on a smaller scale.

In a multi-agent ticket resolution system I built with LangGraph, agents could resolve routine cases, but anything sensitive waited for human approval, and a 60-case golden test set caught regressions. At my job as AI Engineer at Project 990 I run an LLM pipeline with an LLM-as-judge layer that checks every output.

Would you have 15 minutes to talk, or could you point me to Saul or whoever is hiring engineers?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Abdel Mahmoud (229 chars): Hi Abdel, Anterior's rule that the AI never denies care is a design choice I respect. I built a LangGraph agent system where sensitive actions wait for human approval, and I'm an AI Engineer at Project 990. Would love to connect.
- Saul Howard (233 chars): Hi Saul, your World's Fair talk on event logs and replay-based evals was great. I built an agent system with a golden test set and human approval steps, and I'm an AI Engineer at Project 990. Open to connecting, and maybe a referral?

## Log
- 2026-11-26 researched
