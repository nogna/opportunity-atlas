# Evidence for an AI guide during Expedition preparation

**Supports:** GitHub issue #6 — research-informed AI guidance for preparing a team-confirmed Expedition  
**Researched:** 2026-07-15  
**Scope:** guidance for choosing and preparing an AI use case; not a claim that a portfolio tool can certify a system as safe or ready to deploy.

## What the guide should help the team do

1. **Choose a narrow, meaningful starting point, then make it real in the workflow.** PwC's first-party research recommends choosing one priority workflow, reviewing it end-to-end, and redesigning handoffs, roles, and throughput rather than merely speeding up a step. It also reports that higher-performing organizations embed AI in standard operating processes. The guide should therefore ask for the *current workflow*, the changed workflow, who performs each handoff, and the intended outcome—not reward a broad collection of disconnected ideas. [PwC, *Want ROI from AI? Go for growth*](https://www.pwc.com/gx/en/1/issues/tech-data-ai/ai-roi.html)

2. **Keep the decision with accountable people.** NIST says accountability structures should give named teams and individuals responsibility for mapping, measuring, and managing AI risks; executive leadership takes responsibility for development/deployment risk decisions. It separately calls for documented human-AI roles and oversight. The guide may explain trade-offs and suggest gaps, but must not rank, confirm, or present a recommendation as the team's decision. [NIST AI RMF Core, Govern 2–3](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

3. **Make the expected benefit and baseline inspectable.** NIST's Map function calls for the business value to be defined, expected benefits and costs compared with appropriate benchmarks, and targeted scope to be documented. Its Measure function calls for context-relevant performance/assurance criteria, documented measures, and monitoring in production. UK government evaluation guidance likewise says to plan evaluation early, state the comparison with business-as-usual, and establish a defined baseline—while recognising that baselines can be difficult when AI changes a complex or subjective activity. During preparation, the guide should prompt for: intended benefit, a present-state baseline (or explicit absence of one), candidate success measure, measurement owner, and known downside/cost. It should not fabricate numbers where evidence is missing. [NIST AI RMF Core, Map 1 & 3; Measure 2](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) and [UK Government, *Guidance on the Impact Evaluation of AI Interventions*](https://www.gov.uk/government/publications/the-magenta-book/guidance-on-the-impact-evaluation-of-ai-interventions-html)

4. **Surface evidence gaps instead of smoothing them over.** NIST requires documenting intended purpose, assumptions/limitations, knowledge limits, use and human oversight; it also says risks or trustworthy characteristics that cannot be measured should be documented. The guide should distinguish evidence from assumptions, flag missing data/validation/owners, and offer a next evidence-gathering action. A gap is a reason for a cautious Expedition or experiment—not an invitation for the AI to invent confidence. [NIST AI RMF Core, Map 1–2; Measure 1](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

5. **Treat the Expedition as a checkpoint, not a deployment approval.** NIST describes Map → Measure → Manage as iterative and says Map must be revisited as context, capabilities, risks, benefits, and impacts change. Its Manage function includes deciding whether development/deployment should proceed based on assessed evidence. An Expedition snapshot can responsibly preserve a team's current priority and its uncertainty, while later delivery governance still performs validation, risk treatment, and go/no-go decisions. [NIST AI RMF Core, lifecycle and Manage 1](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

## Proposed first-guide behavior

When someone opens **Prepare Expedition**, show a quiet, dismissible briefing for each leading Island that contains:

- the workflow and outcome already stated, plus a clear "not yet stated" signal where absent;
- the proposed evidence, baseline, success measure, and accountable owner—each marked as **provided**, **assumption**, or **missing**;
- a short explanation of the ranking trade-off based only on the Map's visible fields and weights;
- one or two optional, concrete actions (for example, "name the workflow owner" or "collect a two-week baseline"); and
- an explicit reminder that the team—not the AI—confirms the Expedition.

This is deliberately advisory. It should neither create delivery tasks automatically nor imply that completing fields satisfies NIST, regulatory, or production-readiness requirements.

## Corroborating first-party industry evidence (context, not normative guidance)

McKinsey's own 2025 survey reports that many organizations remain in experimentation or pilot stages and have not embedded AI deeply enough in workflows to realize material enterprise-level benefits. Its prior survey lists workflow redesign, feedback mechanisms, active leaders, and well-defined KPIs among adoption-and-scaling practices. These surveys support the product's focus on workflow, ownership, feedback, and measures, but are self-reported industry research—not a safety or compliance standard. [McKinsey, *The State of AI: Global Survey 2025*](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) and [McKinsey, *How organizations are rewiring to capture value*](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-how-organizations-are-rewiring-to-capture-value)

## Source selection note

The user-supplied Notion briefing was used only to identify themes. This note links directly to the original publishers: NIST and UK Government publications are official guidance; PwC and McKinsey are the original publishers of the cited survey/advisory findings.
