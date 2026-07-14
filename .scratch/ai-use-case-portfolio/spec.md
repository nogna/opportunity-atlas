# AI Use-Case Portfolio

Status: ready-for-agent

## Problem Statement

AI teams, their business stakeholders, and cross-functional partners need to decide which AI use case to pursue next. Today, discovery notes and evaluation criteria commonly end up in spreadsheets or scattered workshop artifacts. Those artifacts are hard to share, do not make assumptions or trade-offs visible, and do not help a group turn a broad set of ideas into an evidence-backed decision.

The group needs a living, visual portfolio that captures shared context, compares opportunities consistently, lets the team adjust its priorities transparently, and preserves why a use case was shortlisted. AI should help people articulate and complete use cases, but must not make an opaque strategic decision for them.

## Solution

Provide a facilitator-led, shareable AI Use-Case Portfolio workspace for the **Work & Productivity** hackathon track. A facilitator enters the team's shared context and manages a portfolio of use cases. The group can scan the portfolio, inspect and shape a shortlisted use case, evaluate candidates against a configurable best-practice rubric, adjust dimension weights, and see an explainable ranked shortlist update immediately.

Each shaped use case describes a clear transformation:

```text
Current workflow / pain → proposed AI-enabled workflow → expected outcome
```

The workspace persists the portfolio, evaluations, configuration, and shortlist rationale as a decision artifact that stakeholders can revisit. AI assistance improves the clarity and completeness of individual entries; human participants retain ownership of the underlying facts, scores, weights, and final decision.

## User Stories

1. As a facilitator, I want to create a portfolio workspace, so that a group has one persistent place to assess AI opportunities.
2. As a facilitator, I want to enter the team's strategic goals, key users, workflows, constraints, and available data, so that every opportunity is evaluated against shared context.
3. As a stakeholder, I want to read the shared context before reviewing ideas, so that I understand the assumptions behind the portfolio.
4. As a facilitator, I want to update the shared context, so that the portfolio remains useful as the team's priorities change.
5. As a facilitator, I want to add a use case with a concise title and initial description, so that brainstorming ideas can enter the portfolio quickly.
6. As a facilitator, I want to record the target user and affected workflow for each use case, so that the group can compare who each opportunity serves.
7. As a facilitator, I want to capture supporting evidence and assumptions for each use case, so that a ranking is not mistaken for proven fact.
8. As a stakeholder, I want to scan all use cases in a compact portfolio board, so that I can compare opportunities without opening a spreadsheet.
9. As a stakeholder, I want to see each use case's stage, evaluation state, and confidence at a glance, so that I can focus discussion on the right candidates.
10. As a facilitator, I want to open a detailed view of one use case, so that I can deepen it without losing the portfolio context.
11. As a facilitator, I want to mark a candidate as discovered, shortlisted, shaped, or not pursuing, so that the portfolio communicates maturity rather than treating every idea equally.
12. As a facilitator, I want to shortlist a promising candidate before completing every detail, so that the group invests its time selectively.
13. As a facilitator, I want to describe the current workflow and pain for a shortlisted use case, so that the problem is concrete before AI is proposed.
14. As a facilitator, I want to describe the proposed AI-enabled workflow, so that the group can discuss what will actually change.
15. As a facilitator, I want to describe the expected outcome and success signal, so that the opportunity has a testable value hypothesis.
16. As a facilitator, I want to record the human role and the proposed AI role, so that the design preserves appropriate human judgement and oversight.
17. As a facilitator, I want AI to turn a rough use-case description into clearer structured language, so that the team can communicate the idea consistently.
18. As a facilitator, I want AI to identify missing information in a use case, so that I can fill gaps before relying on an evaluation.
19. As a facilitator, I want to accept, edit, or reject AI-generated suggestions, so that the artifact reflects the team's actual judgement.
20. As a stakeholder, I want AI suggestions to be visibly distinct from team-authored content, so that I can evaluate their provenance.
21. As a facilitator, I want the portfolio to begin with a best-practice set of AI-use-case evaluation dimensions, so that the group has a credible starting point.
22. As a facilitator, I want to rename, add, remove, and reorder evaluation dimensions, so that the rubric fits the organization's context.
23. As a facilitator, I want to assign an understandable weight to each dimension, so that the ranking reflects the group's current priorities.
24. As a facilitator, I want to score each use case against each applicable dimension and add a rationale, so that the score is inspectable.
25. As a facilitator, I want to identify my confidence in an evaluation, so that weak evidence is visible instead of hidden in a single number.
26. As a stakeholder, I want to see the default dimensions—expected value, strategic alignment, data readiness, delivery effort, risk, and confidence in evidence—so that I understand the initial best-practice framing.
27. As a stakeholder, I want to understand whether a higher or lower score is favourable for a dimension, so that I can interpret the ranking correctly.
28. As a facilitator, I want changing a dimension's weight to update the portfolio ranking immediately, so that the group can explore trade-offs live.
29. As a stakeholder, I want to see why a use case has its current rank, so that I can challenge the inputs rather than distrust an opaque score.
30. As a stakeholder, I want to compare each use case's dimension scores and rationales, so that I can distinguish a quick win from a strategic bet.
31. As a facilitator, I want to select a next use case to pursue and record the decision rationale, so that the group leaves with a concrete outcome.
32. As a stakeholder, I want the shortlisted decision and rationale to persist when I return, so that the artifact supports follow-up conversations.
33. As a facilitator, I want viewers to see portfolio changes during a review session, so that the workspace supports a shared live decision conversation.
34. As a viewer, I want to review the current state without editing it, so that the MVP has clear facilitator-led collaboration boundaries.
35. As a judge, I want a complete sample portfolio with several credible AI opportunities, so that I can understand and test the product without entering data.
36. As a judge, I want a clear end-to-end path from shared context through a ranked shortlist, so that I can see this is a working product rather than a static visualization.
37. As a project author, I want to explain how GPT-5.6 contributes to structured drafting and gap identification, so that the submission meets the hackathon's tool-use requirement.
38. As a project author, I want to document how Codex was used to build the project, so that the final submission can truthfully provide the required evidence.

## Implementation Decisions

- Model the product as one portfolio-workspace boundary. This boundary owns shared context, use cases, evaluation dimensions, weights, assessments, ranking, shortlist state, and decision rationale. Presentation views and AI assistance interact with this boundary instead of creating competing state models.
- Implement the application domain and server-side capabilities in Python. Select the specific web framework, persistence library, and frontend approach during implementation planning; those choices must preserve the single portfolio-workspace boundary and the facilitator/viewer interaction model.
- Persist a single demonstrable workspace with seeded sample data. The implementation may support multiple workspaces internally, but multi-tenant administration is not required for the MVP.
- A use case contains: identity and stage; target user and affected workflow; initial description; current workflow/pain; proposed AI-enabled workflow; expected outcome; human role; AI role; evidence; assumptions; risks; evaluation assessments; and shortlist/decision rationale.
- Stages are `discovered`, `shortlisted`, `shaped`, and `not pursuing`. A use case may be evaluated while discovered or shortlisted; the richer current-to-AI workflow fields are expected when it is shaped.
- Seed the workspace with an editable default rubric: expected value, strategic alignment, data readiness, delivery effort, risk, and confidence in evidence. Each dimension has a name, explanation, direction of desirability, weight, and display order.
- Represent each assessment as a score on a documented common scale, an optional rationale, and a confidence indicator. The system must preserve raw assessments separately from calculated rank.
- Calculate a transparent weighted ranking from dimension assessments and current weights. Dimensions whose lower values are better must be normalized before aggregation. Show the factors contributing to a use case's ranking in the interface.
- Weight changes update the derived ranking immediately and do not silently rewrite the underlying assessments or previously recorded decision rationale.
- Make scores, weights, rationales, and the final shortlist editable by the facilitator. A viewer can see the same persisted workspace and updates but has no editing controls in the MVP.
- Treat AI assistance as a bounded drafting service. It receives the relevant shared context and selected use-case content, returns suggested structured wording and missing-context prompts, and never writes portfolio data without facilitator review.
- Ensure the interaction distinguishes AI suggestions from accepted portfolio content and supports accepting, editing, or discarding each suggestion.
- Provide a portfolio board as the primary scan-and-compare view, a detailed shaping view for an individual use case, and an evaluation/prioritization view or panel. The exact visual style is implementation-led, but it must be visibly more useful for comparison than a plain spreadsheet.
- The demonstrable live-collaboration model is facilitator-led: edits are made by one facilitator and changes propagate to viewers. Concurrent edits to the same field, cursors, presence, and conflict resolution are not required.
- Include a realistic, neutral sample organization and six to eight opportunities so the demo can show comparison, shaping, reweighting, and selection without requiring user setup.
- Design the demo path around a complete, judge-testable flow: inspect context, compare opportunities, shape one candidate, review its evaluation rationale, adjust weights, and record a shortlist decision.
- Record the project’s use of Codex and GPT-5.6 in the README and submission materials. The public demo must show a working experience and accurately explain both uses.

## Testing Decisions

- Test external portfolio behaviour, not implementation details. A good test proves what a facilitator or viewer can observe: stored content, ranking results, visibility of rationale, allowed edits, and decision persistence.
- Test the portfolio-workspace boundary as the highest seam. Cover creation/loading of context and use cases, stage transitions, rubric edits, score updates, ranking recalculation, and shortlist decision recording through its public operations.
- Test weighted ranking with representative mixtures of positive-direction and inverse-direction dimensions, zero and changed weights, incomplete assessments, equal scores, and deterministic tie handling.
- Test that weight changes alter derived ordering while leaving raw assessment data intact.
- Test that a score's rationale and confidence are returned with the relevant use case, so that ranking explanations cannot lose their evidence context.
- Test AI-assistance requests at the service boundary with controlled responses. Verify that suggestions are clearly presented for review and that no suggestion becomes persisted use-case content until the facilitator explicitly accepts or edits it.
- Test facilitator and viewer behaviour at the UI boundary: viewers can inspect updates but cannot invoke editing actions; facilitators can complete the end-to-end portfolio flow.
- Add end-to-end coverage for the demo path: load seeded workspace, inspect portfolio, shape a candidate, change a weight, observe the ranking update, and save a shortlist rationale.
- There is no existing test prior art in this repository. Establish focused domain/interaction tests around the portfolio-workspace boundary and a small set of end-to-end tests around the visible workflow.

## Out of Scope

- Importing spreadsheets, documents, notes, images, or workshop artifacts.
- Tracking deployed model or agent quality, cost, latency, or human-override performance.
- AI-driven portfolio blind-spot analysis, duplicate detection, or opportunity discovery recommendations.
- Multiple saved named evaluation lenses.
- A configurable multi-axis opportunity map or advanced animated visualizations beyond what is necessary to demonstrate ranking updates.
- Simultaneous multi-user editing, presence indicators, cursors, merge/conflict handling, and fine-grained permissions.
- Industry-specific templates, integrations, and enterprise identity/administration.
- Building, deploying, or evaluating the selected AI solution itself; the product helps decide what to pursue.

## Further Notes

- Recommended hackathon track: **Work & Productivity**.
- The project must remain a runnable, non-trivial product. The portfolio board alone is insufficient; judges should be able to complete the full decision flow.
- The intended submission needs a public sub-three-minute YouTube demo with audio, a repository and README, and the `/feedback` Codex Session ID for the primary build thread. Consult `docs/research/openai-build-week.md` before implementation and submission planning.
- This spec synthesizes `docs/planning/ai-use-case-portfolio.md`. That note remains the record of the discovery interview and deferred ideas.
