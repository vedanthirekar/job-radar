# WorkOS
- Site: workos.com · San Francisco, CA · size 48 (Built In, may be out of date) · 3 tech H-1B filings
- What they do: APIs that make apps enterprise-ready: SSO, SCIM directory sync, AuthKit login, audit logs, and now auth for AI agents and MCP servers.
- Hook: "Scaling events and webhooks: from sync to async, in order" by Yong Wang (Nov 24, 2026): outbox table plus CDC onto Kinesis and SQS FIFO queues; each event's ordering key is its "dependency root" (membership events key on the user, not the group, to avoid a hot key); idempotent capture worker claims the event ID first.
- Hook source: https://workos.com/blog/events-webhooks-sync-to-async-in-order
- Vedant's angle: multi-agent ticket resolution project built on FastAPI with a PostgreSQL job queue (retries, idempotency).

## People
- Michael Grinich, CEO · LinkedIn: not found · source: https://sacra.com/research/michael-grinich-workos-enterprise-ready-at-launch/ (email: pending Apollo)
- Yong Wang, Engineer (author of the events and webhooks post; title not shown) · LinkedIn: not found · source: https://workos.com/blog/events-webhooks-sync-to-async-in-order (email: pending Apollo)
- Notes: No CTO found. CEO chosen because Built In lists under 50 people.

## Email draft
To: Michael Grinich
Subject: Dependency roots in WorkOS events

Hi Michael,

Yong Wang's post on moving events and webhooks to async had a detail I keep thinking about: each event's ordering key is its "dependency root," so a membership event keys on the user instead of the group to avoid a hot key. That keeps order without serializing everything.

I'm an AI Engineer at Project 990. On the side I built a multi-agent ticket system on FastAPI with a PostgreSQL job queue, and keeping retries idempotent was the hardest part to get right.

Would you be open to a 15-minute chat, or could you point me to the right person on the engineering team?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Michael Grinich (219 chars): Hi Michael, Yong Wang's post on keying WorkOS events by dependency root was a great read. I'm an AI Engineer at Project 990 and have built job queues where ordering and retries were the hard part. Would love to connect.
- Yong Wang (250 chars): Hi Yong, your post on moving WorkOS events to async while keeping order was great, especially keying memberships on the user to dodge hot keys. I'm an AI Engineer at Project 990. Would you be open to connecting, and maybe a referral if there's a fit?

## Log
- 2026-11-27 researched
