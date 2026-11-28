# Socket
- Site: socket.dev · San Francisco, CA · size 20-100 (Employbl) · 1 tech H-1B filings
- What they do: Software supply chain security that detects and blocks malicious or risky open source packages (npm, PyPI, RubyGems, extensions) before they reach your code.
- Hook: "Microsoft's agent-framework PyPI package Compromised with Credential Stealer" (Nov 17, 2026, Socket Research Team): versions 1.26.1 and 1.26.2 used Python startup hooks to collect credentials and environment data (Azure in both, GitHub Actions OIDC in 1.26.2) and sent it to a webhook.site endpoint.
- Hook source: https://socket.dev/blog/agent-framework-pypi-package-compromised-with-credential-stealer (summary and date: https://www.plushcap.com/content/socket/blog/socket-microsofts-agent-framework-pypi-package-compromised-with-credential-stealer)
- Vedant's angle: Python LLM stack at Project 990 and the LangGraph multi-agent project, both full of packages that sit next to API keys.

## People
- Feross Aboukhadijeh, Founder and CEO · LinkedIn: not found · source: https://www.employbl.com/companies/socket (email: pending Apollo)
- Karlo Zanki, Threat researcher (author of the LiteLLM and GitHub Actions hardening posts; title not shown) · LinkedIn: not found · source: https://www.plushcap.com/companies/socket/blog (email: pending Apollo)
- Notes: No CTO found. CEO chosen because size is listed as 20-100. Recent news: $60M Series C at $1B valuation (May 20, 2026).

## Email draft
To: Feross Aboukhadijeh
Subject: The agent-framework startup hook

Hi Feross,

Socket's November 17 write-up on Microsoft's agent-framework package stood out to me: versions 1.26.1 and 1.26.2 used Python startup hooks to collect credentials, and 1.26.2 also went after GitHub Actions OIDC. Agent libraries are exactly what people like me install without a second look.

I'm an AI Engineer at Project 990, running LLM pipelines with open-source models on a GPU cluster, and on the side I built a multi-agent ticket system in LangGraph. Both pull in a long list of Python packages that live right next to API keys.

Would you be open to a 15-minute chat about engineering roles at Socket?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Feross Aboukhadijeh (223 chars): Hi Feross, the agent-framework PyPI write-up was a wake-up call, since agent libraries sit right next to API keys. I'm an AI Engineer at Project 990 building LLM pipelines and agent systems in Python. Would love to connect.
- Karlo Zanki (232 chars): Hi Karlo, your posts on the LiteLLM compromise and hardening GitHub Actions were great reads. I'm an AI Engineer at Project 990 working on Python LLM pipelines. Would you be open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-27 researched
