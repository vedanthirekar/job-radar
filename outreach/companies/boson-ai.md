# Boson AI
- Site: boson.ai · Santa Clara, CA (also Toronto) · size ~21 (Built In) · 8 tech H-1B filings
- What they do: Builds voice and video AI models (Higgs Audio TTS, Higgs Realtime speech-to-speech, Higgs Avatar) for enterprise voice agents, including on-premises deployment.
- Hook: Higgs Realtime Duplex research preview (Nov 9, 2026): Boson's first full-duplex model, a 45B mixture-of-experts front model that reasons and calls tools itself and hands harder requests to a larger backend model; streams input in 160ms chunks and scores 98.9 on Big Bench Audio. Alex Smola: "Our 45B model holds its own against one six times its size."
- Hook source: https://audioxpress.com/news/boson-ai-previews-higgs-realtime-duplex-for-conversational-voice-and-video-agents
- Vedant's angle: Methix, routing simple requests to a cheaper model (about 20% lower Azure costs).

## People
- Mu Li, Co-founder & CTO · LinkedIn: not found · source: https://www.crunchbase.com/person/mu-li-afe2 (email: pending Apollo)
- Alex Smola, Co-founder & CEO · LinkedIn: not found · source: https://audioxpress.com/news/boson-ai-previews-higgs-realtime-duplex-for-conversational-voice-and-video-agents (email: pending Apollo)
- Notes: Both ex-AWS. Higgs Audio v3 TTS contributors listed at https://www.lmsys.org/blog/2026-06-04-higgs-audio-v3-tts (June 4, 2026). Raised $70M (Fortune, July 27, 2026).

## Email draft
To: Mu Li
Subject: The 45B front model in Higgs Realtime Duplex

Hi Mu,

The Higgs Realtime Duplex preview has a design choice I liked: a 45B mixture-of-experts front model that reasons and calls tools itself, handing harder requests to a larger backend model.

I did a small version of that split at Methix, where I built an AI assistant for music artists on Azure OpenAI and routed simple requests to a cheaper model, which cut Azure costs about 20%. Now I'm an AI Engineer at Project 990, running open-source models on a GPU cluster for 175,000+ nonprofits.

Would you be open to a 15-minute chat about engineering roles at Boson AI?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Mu Li (224 chars): Hi Mu, the Higgs Realtime Duplex split between a 45B front model and a larger backend is a smart design. I routed easy requests to a cheaper model at Methix and now run open-source LLMs at Project 990. Would love to connect.
- Alex Smola (229 chars): Hi Alex, congrats on the Higgs Realtime Duplex preview; a 45B model holding its own against one six times its size is impressive. I'm an AI Engineer at Project 990 running open-source LLMs on a GPU cluster. Would love to connect.

## Log
- 2026-11-27 researched
