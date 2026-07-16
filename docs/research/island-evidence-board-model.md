# Island Evidence board — research-backed information model

**Issue:** [#24](https://github.com/nogna/opportunity-atlas/issues/24)  
**Status:** research finding; not a product decision  
**Retrieved:** 2026-07-16

## Question

What is the smallest progressive information model for an Island's Evidence board
that helps a team develop an AI use-case opportunity without turning early
exploration into paperwork or allowing generated claims to masquerade as evidence?

## Source-backed conclusion

The common thread is not "collect a larger use-case form." McKinsey identifies
workflow redesign as the surveyed attribute with the largest effect on reported
gen-AI EBIT impact, alongside feedback mechanisms, trust, and well-defined KPIs.
PwC likewise argues that higher returns come from changing how value is created,
redesigning a priority workflow end-to-end, and pairing a named owner with success
metrics. Deloitte warns that isolated use cases fail to scale when process, data,
controls, roles, and skills are not considered together.

**Design inference:** an Evidence board should make the team's *opportunity
hypothesis* inspectable: a real workflow problem, a proposed AI-enabled change,
the value/evidence that would test it, and the readiness/risk conditions that could
invalidate it. It should progressively reveal the rest rather than require a full
business case at Island creation.

## Recommended progressive model

### Core: required to create a credible Island

| Board section | Minimum team-authored content | Why it is core |
| --- | --- | --- |
| **Provenance** | The preserved Scouting note, plus a short team framing of what it prompted them to explore | Keeps the early observation visible without treating it as verified fact. |
| **Workflow/problem today** | Who does what today, where the friction or decision is, and who is affected | Anchors the opportunity in a real workflow rather than an AI capability. |
| **AI-enabled change** | A tentative description of how AI could change a step, handoff, decision, or human role | Tests redesign of work, not a generic "add AI" idea. |
| **Possible outcome** | One observable or measurable benefit the team hopes to create | Gives exploration a value direction without demanding a formal ROI model. |
| **Evidence and unknowns** | At least one observation/source and the most important unanswered question or assumption | Makes confidence and missing knowledge explicit instead of allowing a polished narrative to imply proof. |

These five sections are sufficient for a team to promote and compare an Island.
They implement the existing domain terms **Scouting note**, **Opportunity
hypothesis**, **Evidence**, and **Value evidence** without confusing a first pass
with delivery approval.

### Evaluation: visible after the hypothesis exists, adjustable by the team

The Evidence board should bring the Map's evaluation values into the same deep-dive
workspace, not create a second ranking system. Start with the current portfolio
rubric and show each value with its rationale:

- expected value and strategic alignment;
- data/technology readiness;
- delivery effort;
- risk; and
- confidence in the evidence.

The values must be editable, explainable, and explicitly attributable to the
team. A value without rationale is weak evidence, so the board should prompt for a
short rationale or link to relevant evidence when a value is changed. This supports
the portfolio's configurable, explainable evaluation model while keeping the
initial hypothesis lightweight.

### Expand when useful, rather than gate promotion

| Progressive section | Use when | Helpful prompts |
| --- | --- | --- |
| **Workflow sketch** | The current change is still vague | Today → AI-enabled change → human review/escalation → outcome. |
| **People and operating change** | Roles, adoption, handoffs, skills, or decision rights will change | Who remains accountable? Who validates, overrides, or receives exceptions? What training/change is needed? |
| **Data and delivery readiness** | The opportunity might move from discovery to delivery | What information is needed, where is it, how reliable/accessible is it, and what integrations or controls are missing? |
| **Risk and safeguards** | The workflow affects people, customers, regulated decisions, sensitive data, or external outputs | What can go wrong, who is harmed, what human review/escalation is required, and who owns it? |
| **Learning plan** | The team is preparing an Expedition | What is the next smallest evidence-seeking action? What result would support, change, or weaken the hypothesis? |
| **Links and supporting material** | There is material worth retaining | Interviews, metrics, policy constraints, examples, and contradictory evidence. |

This provides depth only where it helps the team make a better next decision. It
should not force a forecast, technical design, or implementation plan merely to
keep an Island on the Map.

## Authorship and AI behaviour

### Team-owned

The team creates, edits, approves, and is shown as the author of:

- the meaning of the Scouting note and the Island's opportunity hypothesis;
- all Evidence, links, observations, and claims of fact;
- evaluation values and their rationale;
- trade-offs, risk acceptance, owners, and promotion/archival decisions.

### AI-guided, never silently authored

AI can offer optional help inside each board section:

- turn rough wording into a proposed hypothesis;
- ask for missing context or distinguish an assumption from an observation;
- propose questions about workflow handoffs, adoption, data, risk, and evidence;
- suggest a small next action to test the hypothesis; and
- explain the existing evaluation rubric or a proposed value change.

Generated text remains an **AI suggestion**, visibly separate until a person
accepts and edits it into team content. The AI should cite only sources supplied
to it or clearly label an uncited statement as a prompt/hypothesis—not Evidence.

## Product safeguards

1. **Provenance is permanent.** Transferring a Scouting note preserves it in the
   Island, with its author/time, as an input—not as evidence or the current
   hypothesis.
2. **Separate facts, assumptions, and AI prompts.** Use distinct visual treatment
   and labels; do not let generated copy be recorded as team Evidence by default.
3. **Require an explicit team action to accept generated material.** Acceptance
   should make the team author/editable content, retaining an audit cue that it
   began as an AI suggestion where useful.
4. **Never let AI modify evaluation values or advance state.** It may explain or
   propose, but it cannot transfer a note, promote/archive an Island, select it
   for an Expedition, or confirm an Expedition.
5. **Ask for provenance for strong claims.** A statement presented as evidence
   should include a source/link, observation owner, or be explicitly marked as an
   assumption to test.
6. **Match checks to risk.** Lightweight low-risk exploration can proceed with
   questions and a next action; sensitive/high-impact opportunities should expose
   risk, human oversight, data, and escalation prompts earlier.

## What this does *not* recommend

- A mandatory ROI spreadsheet or full implementation case before an Island can
  exist.
- A fixed AI-generated score, opaque priority recommendation, or AI-authored
  Evidence.
- Treating every opportunity as a pilot. An Island is a living opportunity
  hypothesis; an Expedition later commits a selected set to evidence-seeking work.
- One universal human/AI operating model. Deloitte explicitly frames the human-AI
  model as a context- and risk-dependent design choice.

## Sources

- McKinsey, [*The state of AI: How organizations are rewiring to capture value*](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-how-organizations-are-rewiring-to-capture-value), March 2025. Workflow redesign, governance, feedback, trust, and KPI practices.
- Deloitte, [*The value beyond the hype: Re-Imagining IT through Operating Model transformation to maximise AI value*](https://www.deloitte.com/uk/en/Industries/technology/perspectives/re-imagining-it-through-operating-model-transformation-to-maximise-ai-value.html), May 2026. Operating-model, data, control, role, skill, maturity, and human-AI collaboration considerations.
- PwC, [*Want ROI from AI? Go for growth*](https://www.pwc.com/gx/en/1/issues/tech-data-ai/ai-roi.html), 2026. Workflow/value redesign, outcome measurement, owners, foundations, and repeatable governance.
- PwC, [*How Responsible AI can create measurable value*](https://www.pwc.com/gx/en/1/issues/c-suite-insights/the-leadership-agenda/ai-responsible.html), November 2025. Value/risk assessment through monitoring, cross-functional ownership, and transparent responsible-AI processes.

## Implication for later product work

This note is research, not an implementation scope. If the team adopts it, the
next decision should specify the minimum first-release fields and what qualifies a
Scouting note for transfer into an Island. That decision belongs in #23 or a new
explicit product-decision issue, not in this research note.
