# Braintrust
- Site: braintrust.dev · unknown (US) · size 11-50 (Himalayas; ~29 in public org chart) · 2 tech H-1B filings
- What they do: An evals and observability platform for LLM and agent apps: evals, tracing, and analysis of production traces (Topics, Patterns, Loop).
- Hook: "Build better agents with Patterns" (Nov 23, 2026): Patterns flagged CI retries resending full context at Notion (saved $1M on coding-agent costs) and surfaced an OpenAI safety-classifier bug quietly degrading ~1% of legal research outputs at Eve.
- Hook source: https://www.braintrust.dev/blog/patterns
- Vedant's angle: Project 990 LLM-as-judge evaluation layer: catching quiet failures in LLM output at scale.

## People
- Ankur Goyal, Co-founder & CEO · LinkedIn: not found · source: https://siliconangle.com/2026/02/17/braintrust-lands-80m-series-b-funding-round-become-observability-layer-ai (email: pending Apollo)
- Notes: No CTO or engineering lead found publicly. Ornella Altunyan wrote the Patterns post (title not listed).

## Email draft
To: Ankur Goyal
Subject: Patterns and the Notion CI retries

Hi Ankur,

The Patterns post stuck with me, especially Notion's CI retries resending full context and the classifier bug at Eve that only touched about 1% of outputs. Quiet failures like that are what I work on every day.

I'm an AI Engineer at Project 990, where I run an open-source LLM pipeline that writes mission statements for 175,000+ nonprofits from IRS filings. I added an LLM-as-judge layer to catch bad outputs before they ship, and it changed how I think about evals.

Would you be open to a 15-minute chat, or could you point me to whoever hires engineers on the evals side?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Ankur Goyal (239 chars): Hi Ankur, the Patterns post on Notion's CI retries and the 1% classifier bug at Eve was great. I built an LLM-as-judge layer for a pipeline covering 175,000+ nonprofits at Project 990 and would love to learn how Braintrust hires engineers.

## Log
- 2026-11-26 researched
