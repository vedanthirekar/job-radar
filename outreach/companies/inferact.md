# Inferact
- Site: inferact.ai · San Francisco, CA · size 11-50 (Simplify) · 8 tech H-1B filings
- What they do: The company started by the vLLM maintainers to build and commercialize the vLLM open-source inference engine.
- Hook: "Introducing vLLM TorchTPU" (Oct 20, 2026, Inferact and Google teams): a new vLLM backend for Google Cloud TPUs built on TorchTPU, shipped as an out-of-tree platform plugin so the scheduler, workers, KV cache manager, and API server stay unmodified upstream vLLM; includes zero-copy KV cache offload to host DRAM and disaggregated prefill/decode with KV resharding.
- Hook source: https://vllm.ai/blog/2026-10-20-vllm-torchtpu
- Vedant's angle: Project 990 runs open-source models (Mistral, Gemma) on a GPU cluster at batch scale for 175,000+ nonprofits.

## People
- Woosuk Kwon, Co-founder & CTO · LinkedIn: not found · source: https://lsvp.com/company/vllm-inferact/ (email: pending Apollo)
- Simon Mo, Co-founder & CEO · LinkedIn: not found · source: https://lsvp.com/company/vllm-inferact/ (email: pending Apollo)
- Notes: Other co-founders: Kaichao You (Chief Scientist), Roger Wang. Raised $150M seed in Jan 2026 (https://techcrunch.com/2026/01/22/inference-startup-inferact-lands-150m-to-commercialize-vllm/). No engineer author found; the TorchTPU post is credited to "Inferact and Google Teams".

## Email draft
To: Woosuk Kwon
Subject: vLLM TorchTPU as an out-of-tree plugin

Hi Woosuk,

The vLLM TorchTPU post made a choice I liked: TPU support ships as an out-of-tree platform plugin, so the scheduler, KV cache manager, and API server stay plain upstream vLLM. Users keep one engine while the hardware underneath changes.

I'm an AI Engineer at Project 990. I run open-source models like Mistral and Gemma on a GPU cluster to write mission statements for 175,000+ nonprofits from IRS filings, so I see the serving layer's behavior at batch scale from the user side.

Would you be open to a 15-minute chat about engineering roles at Inferact?

I'm on STEM OPT, so no visa sponsorship is needed for up to three years.

Vedant Hirekar · vedanthirekar.com

## LinkedIn notes
- Woosuk Kwon (216 chars): Hi Woosuk, shipping TPU support as an out-of-tree plugin with upstream vLLM untouched is a clean call. I run open-source models on a GPU cluster at batch scale as an AI Engineer at Project 990. Would love to connect.
- Simon Mo (204 chars): Hi Simon, the vLLM TorchTPU launch with Google was great to see. I'm an AI Engineer at Project 990 running open-source models like Mistral and Gemma at batch scale on a GPU cluster. Would love to connect.

## Log
- 2026-11-27 researched
