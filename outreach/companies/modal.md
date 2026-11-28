# Modal
- Site: modal.com · New York, NY (also San Francisco, Stockholm, London) · size ~150-200 (TrueUp) · 12 tech H-1B filings
- What they do: A serverless cloud for AI workloads: GPU functions, inference endpoints, training, and sandboxes for running agent code.
- Hook: "Sandbox resourcing: burst, don't reserve" (Nov 12, 2026): a typical Sandbox spends more than half its life under 6% of peak CPU, so Sandboxes now start at a 0.125-core request and burst up to 16 cores, billed at the higher of request or use; a 20-minute coding-agent run costs 8.4 cents per Sandbox-hour versus 20.0 cents reserved (58% less).
- Hook source: https://modal.com/blog/sandbox-bursting
- Vedant's angle: multi-agent ticket resolution project (LangGraph, PostgreSQL job queue, human approval), where agents mostly wait on model calls; plus the Project 990 GPU pipeline.

## People
- Akshat Bubna, Co-founder & CTO · LinkedIn: not found · source: https://latent.space/wiki/akshat-bubna-6d4b6f6d/ (email: pending Apollo)
- Kevin Yang, Engineer (author of the Sandbox bursting post) · LinkedIn: not found · source: https://modal.com/blog/sandbox-bursting (email: pending Apollo)
- Notes: CEO: Erik Bernhardsson (https://modal.com/company).

## Email draft
To: Akshat Bubna
Subject: Burst, don't reserve

Hi Akshat,

Kevin Yang's post on Sandbox bursting had a striking number: a typical Sandbox spends more than half its life under 6% of peak CPU. For agents waiting on model calls, reserving is the wrong default.

I'm an AI Engineer at Project 990, running an LLM pipeline on a GPU cluster that writes mission statements for 175,000+ nonprofits. On the side I built a multi-agent ticket resolution system on a PostgreSQL job queue, and its agents sit idle most of the time, waiting on the model or a human approval.

Would you be open to a 15-minute chat about engineering roles at Modal?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Akshat Bubna (241 chars): Hi Akshat, the Sandbox bursting post made a strong case: most agent sandboxes sit under 6% of peak CPU. I'm an AI Engineer at Project 990 running an LLM pipeline on a GPU cluster, and I build agent systems on the side. Would love to connect.
- Kevin Yang (262 chars): Hi Kevin, enjoyed your post on Sandbox bursting, especially the coding-agent trace where CPU stayed near zero between pytest spikes. I'm an AI Engineer at Project 990 building LLM pipelines. Would you be open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-27 researched
