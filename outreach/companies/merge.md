# Merge
- Site: merge.dev · San Francisco, CA (plus New York) · size 115 employees (Built In NYC) · 11 tech H-1B filings
- What they do: A unified API for B2B integrations (HRIS, ATS, CRM, accounting, and more) plus Agent Handler, which gives AI agents governed tool access to third-party apps.
- Hook: "Use your existing credentials with Merge Agent Handler" (Nov 19, 2026) by Matt Linehan: passthrough auth lets a product send the end user's OAuth token or API key in an X-Tool-Auth header per MCP session; Merge strips the header before logging, never stores it, and drops authenticate_* tools from tools/list.
- Hook source: https://www.merge.dev/blog/merge-agent-handler-passthrough
- Vedant's angle: Multi-agent ticket resolution side project (LangGraph, FastAPI) where sensitive tool actions wait for human approval.

## People
- Gil Feig, Co-founder & CTO · LinkedIn: not found · source: https://jam.dev/blog/how-merge-uses-ai-w-co-founder-cto-gil-feig/ (email: pending Apollo)
- Matt Linehan, Product Manager (author of the passthrough post) · LinkedIn: not found · source: https://www.merge.dev/blog/merge-agent-handler-passthrough (email: pending Apollo)

## Email draft
To: Gil Feig
Subject: Passthrough auth in Agent Handler

Hi Gil,

Passthrough auth for Agent Handler is a sensible call: the product keeps its own OAuth flows, sends the token in X-Tool-Auth, and Merge strips the header before logging. Dropping the authenticate tools from tools/list once it's on is a nice touch.

I'm an AI Engineer at Project 990. On the side I built a multi-agent ticket resolution system with LangGraph and FastAPI, where any sensitive tool action waits for human approval, so who an agent acts as and what it may touch is a question I've had to answer.

Would you be open to a 15-minute chat about engineering roles at Merge?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Gil Feig (213 chars): Hi Gil, stripping X-Tool-Auth before logging in the new Agent Handler passthrough is a careful detail. I built a multi-agent ticket system where sensitive tool calls wait for human approval. Would love to connect.
- Matt Linehan (239 chars): Hi Matt, enjoyed your post on passthrough credentials for Agent Handler. I'm an AI Engineer at Project 990 and built an agent system with gated tool calls on the side. Would you be open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-27 researched
