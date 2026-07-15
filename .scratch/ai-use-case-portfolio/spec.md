# AI Use-Case Portfolio

Status: ready-for-agent

## Problem Statement

AI teams, their business stakeholders, and cross-functional partners need to decide which AI use case to pursue next. Today, discovery notes and evaluation criteria commonly end up in spreadsheets or scattered workshop artifacts. Those artifacts are hard to share, do not make assumptions or trade-offs visible, and do not help a group turn a broad set of ideas into an evidence-backed decision.

The group needs a living, visual portfolio that captures shared context, compares opportunities consistently, lets the team adjust its priorities transparently, and preserves why a use case was shortlisted. AI should help people articulate and complete use cases, but must not make an opaque strategic decision for them.

## Solution

Provide a collaborative, shareable AI Use-Case Portfolio workspace for the **Work & Productivity** hackathon track. Team members enter shared context and manage a portfolio of use cases. The group can scan the portfolio, inspect and shape a shortlisted use case, evaluate candidates against a configurable best-practice rubric, adjust dimension weights, and see an explainable ranked shortlist update immediately.

Each shaped use case describes a clear transformation:

```text
Current workflow / pain → proposed AI-enabled workflow → expected outcome
```

The workspace persists the portfolio, evaluations, configuration, and shortlist rationale as a decision artifact that stakeholders can revisit. AI assistance can propose candidate Opportunities from the Decision frame and improve the clarity and completeness of individual entries; human participants retain ownership of the underlying facts, scores, weights, and final decision.

## User Stories

1. As a team member, I want to open the shared portfolio Workspace and its current Iteration, so that a group has one persistent place to assess AI opportunities.
2. As a team member, I want to capture and update a shared Decision frame—including strategic goals, key users, workflows, constraints, and available data—so that every Opportunity is evaluated against shared context.
3. As a team member, I want to start the Decision frame broad or narrow and leave unknown prompts incomplete, so that the team can focus its context progressively without blocking Opportunity discovery.
4. As a stakeholder, I want to read the shared Decision frame before reviewing ideas, so that I understand the assumptions behind the portfolio.
5. As a team member, I want to add an Opportunity with a concise title and initial description, so that brainstorming ideas can enter the portfolio quickly.
6. As a team member, I want AI to propose candidate Opportunities from the Decision frame with explicit assumptions and uncertainties, so that the group can explore starting points without treating generated content as fact or a decision.
7. As a team member, I want to correct, add evidence to, and explicitly add or discard each proposed candidate, so that only team-reviewed Opportunities enter the portfolio.
8. As a team member, I want to choose whether AI asks clarifying questions before generating candidates or generates assumption-labelled drafts immediately, so that incomplete context does not block progress.
9. As a team member, I want to record the target user and affected workflow for each Opportunity, so that the group can compare who each opportunity serves.
10. As a team member, I want to capture team-authored Evidence notes and optional links for each Opportunity, so that a Ranking is not mistaken for proven fact.
11. As a stakeholder, I want to scan all Opportunities in a compact portfolio board, so that I can compare opportunities without opening a spreadsheet.
12. As a stakeholder, I want to see each Opportunity's derived completeness, evaluation state, and Evidence confidence at a glance, so that I can focus discussion on the right candidates.
13. As a team member, I want to open a detailed view of one Opportunity, so that I can deepen it without losing the portfolio context.
14. As a team member, I want to record why an Opportunity is not being pursued, so that the portfolio preserves that decision without a general lifecycle status.
15. As a team member, I want to shortlist a promising Opportunity before completing every detail, so that the group invests its time selectively.
16. As a team member, I want to describe the current workflow and pain for a shortlisted Opportunity, so that the problem is concrete before AI is proposed.
17. As a team member, I want to describe the proposed AI-enabled workflow, so that the group can discuss what will actually change.
18. As a team member, I want to describe the expected outcome and success signal, so that the Opportunity has a testable value hypothesis.
19. As a team member, I want to record the human role and the proposed AI role, so that the design preserves appropriate human judgement and oversight.
20. As a team member, I want AI to turn a rough Opportunity description into clearer structured language, so that the team can communicate the idea consistently.
21. As a team member, I want AI to identify missing information in an Opportunity, so that I can fill gaps before relying on an evaluation.
22. As a team member, I want to accept, edit, or reject AI-generated suggestions, so that the artifact reflects the team's actual judgement.
23. As a stakeholder, I want AI suggestions to be visibly distinct from team-authored content, so that I can evaluate their provenance.
24. As a team member, I want the portfolio to begin with a best-practice set of AI-use-case Evaluation dimensions, so that the group has a credible starting point.
25. As a team member, I want to rename, add, and reorder Evaluation dimensions, and set a dimension's weight to zero, so that the rubric fits the organization's context without removing its default framing.
26. As a team member, I want to assign an understandable weight to each Evaluation dimension, so that the Ranking reflects the group's current priorities.
27. As a team member, I want to score each Opportunity against each applicable Evaluation dimension and add a rationale, so that the score is inspectable.
28. As a team member, I want to identify my confidence in an Assessment, so that weak evidence is visible instead of hidden in a single number.
29. As a team member, I want an Opportunity with missing weighted Assessments to be visibly unranked, so that incomplete evidence is not mistaken for a competitive result.
30. As a stakeholder, I want to see the default Evaluation dimensions—expected value, strategic alignment, data readiness, delivery effort, risk, and confidence in evidence—so that I understand the initial best-practice framing.
31. As a stakeholder, I want to understand whether a higher or lower score is favourable for an Evaluation dimension, so that I can interpret the Ranking correctly.
32. As a team member, I want changing an Evaluation dimension's weight to update the portfolio Ranking immediately, so that the group can explore trade-offs live.
33. As a team member, I want AI to suggest Evaluation-dimension weight changes from the Decision frame, so that the group can consider a context-specific starting point without surrendering judgement.
34. As a team member, I want to see AI-proposed weights as muted initial values in the relevant fields and reveal their Decision-frame rationale on hover, so that I can inspect the recommendation without cluttering the comparison view.
35. As a team member, I want to apply an entire AI-proposed weight set with one action, while retaining the ability to adjust individual weights afterward, so that the group can adopt a coherent starting point without losing control.
36. As a stakeholder, I want to see why an Opportunity has its current rank, so that I can challenge the inputs rather than distrust an opaque score.
37. As a stakeholder, I want to compare each Opportunity's Assessment scores and rationales, so that I can distinguish a quick win from a strategic bet.
38. As a team member, I want to select a next Opportunity to pursue and record a required short, human-written decision rationale, so that the group leaves with a concrete outcome that explains trade-offs beyond the Ranking and sets the Iteration as a fixed record.
39. As a team member, I want to select an unranked Opportunity when necessary, with its missing Assessments clearly shown and the required rationale explaining the override, so that the Ranking informs rather than vetoes human judgement.
39. As a team member, I want AI to surface trade-offs among shortlisted Opportunities without recommending or selecting the next one, so that the final decision remains the team's judgement.
40. As a stakeholder, I want set Iterations to remain visible with their Next Opportunity decision, rationale, and Ranking snapshot, so that later reassessment does not erase history.
41. As a stakeholder, I want a Next Opportunity decision to preserve its Ranking and weights at the moment its Iteration is set, so that the completed decision remains explainable.
42. As a stakeholder, I want the shortlisted decision and rationale to persist when I return, so that the artifact supports follow-up conversations.
43. As a team member, I want to see portfolio changes during a review session, so that the Workspace supports a shared live decision conversation.
44. As a team member, I want edits to auto-save while other team members continue working elsewhere, so that the group can collaborate without competing writes to the same field or a Save button.
45. As a team member, I want to see when a field is being edited by someone else, so that I know why I cannot edit it until its temporary lock is released.
46. As a team member, I want to choose a display name when opening the Workspace, so that collaborators can identify my field-level edit locks without an account.
47. As a judge, I want a complete sample portfolio with several credible AI opportunities, so that I can understand and test the product without entering data.
48. As a judge, I want a clear end-to-end path from shared context through a ranked shortlist, so that I can see this is a working product rather than a static visualization.
49. As a project author, I want to explain how GPT-5.6 contributes to structured drafting and gap identification, so that the submission meets the hackathon's tool-use requirement.
50. As a project author, I want to document how Codex was used to build the project, so that the final submission can truthfully provide the required evidence.

## Implementation Decisions

- Model the product as one portfolio-workspace boundary. This boundary owns the Decision frame, Opportunities, Evaluation dimensions, weights, Assessments, Ranking, Shortlist, and Next Opportunity decision. Presentation views and AI assistance interact with this boundary instead of creating competing state models.
- Model the Workspace as ordered Iterations. The current Iteration is a long-lived, editable draft that owns its Decision frame, Opportunities, Evaluation dimensions, weights, Assessments, Ranking, Shortlist, and Archive decisions. It may evolve throughout an exploratory or evaluation phase without creating versions.
- Recording a Next Opportunity decision sets the current Iteration as read-only and preserves its decision, rationale, and Ranking snapshot. A new Iteration starts only from that set current Iteration with a carry-forward review: it records inherited Opportunities the team archives, with a reason, and copies the kept Decision frame, Opportunities, Evidence, rubric, weights, and Assessments as an editable starting point.
- An archived inherited Opportunity may be restored while the new Iteration is a draft; record the restoration in that Iteration.
- An Archive decision shows a compact read-only summary of the inherited Opportunity and links to its source Iteration.
- During the carry-forward review, AI may flag inherited Opportunities that may no longer fit the reassessment trigger. It must label assumptions and uncertainties and cannot archive, restore, or otherwise change an Opportunity; the team explicitly keeps, archives, or restores each one.
- An Opportunity marked not-pursuing in the source Iteration is not automatically archived. Show it in carry-forward review as previously set aside and require the team to explicitly keep or archive it.
- An Iteration remains a draft until it records one Next Opportunity decision. If no candidate is suitable, continue the draft and record not-pursuing decisions rather than setting an empty Iteration.
- Iterations form one linear history; branching from an older Iteration is out of scope for the MVP.
- Make each Iteration's source Iteration and creation time prominent in the artifact history; do not emphasize who started it.
- Require a short “what changed?” note when starting a new Iteration, and display it with the Iteration's source and creation time.
- Give each Iteration an automatic sequential name and allow the team to add an optional custom name.
- Permit a custom Iteration name to change only while the Iteration is a draft; fix it when the Iteration is set.
- Implement the application domain and server-side capabilities in Python. Select the specific web framework, persistence library, and frontend approach during implementation planning; those choices must preserve the single portfolio-workspace boundary and collaborative field-lock interaction model.
- Persist one pre-created, demonstrable Workspace with a seeded current Iteration. Workspace creation, selection, and tenant separation are out of scope for the MVP.
- Ask each person to choose a display name when opening the Workspace and retain it in that browser. No accounts, invitations, roles, or identity administration are required for the MVP.
- An Opportunity contains: identity; target user and affected workflow; initial description; current workflow/pain; proposed AI-enabled workflow; expected outcome; human role; AI role; Evidence; assumptions; risks; Assessments; and shortlist or not-pursuing decision rationale.
- Evidence consists of team-authored notes and optional links. AI may structure or question Evidence, but it must not present unverified external research or generated citations as Evidence in the MVP.
- Do not maintain a general Opportunity lifecycle stage. Derive maturity from the Opportunity's content and Assessment coverage; the richer current-to-AI workflow fields are expected for a shaped Opportunity. A not-pursuing decision explicitly records when an Opportunity is set aside and why; it is reversible while the Iteration is a draft, and reconsideration after an Iteration is set happens in a new Iteration.
- A Shortlist is a manually curated set of promising Opportunities for focused comparison within an Iteration. The team may record one next Opportunity to pursue from that Shortlist, with a required short, human-written rationale. Later reassessment starts a new Iteration rather than rewriting the prior decision; neither record is a lifecycle stage.
- Decision records include the Team member's chosen display name and an automatic timestamp.
- Seed the Workspace with an editable default rubric: expected value, strategic alignment, data readiness, delivery ease, risk manageability, and Evidence confidence. Each Evaluation dimension has a name, concise definition, 1, 3, and 5 scoring anchors, direction of desirability, weight, and display order. The default dimensions all use 5 as their most favourable score; custom dimensions may define an inverse direction when necessary.
- Default Evaluation dimensions remain present in an Iteration. Teams may rename, reorder, add custom dimensions, and set a dimension's weight to zero, but do not remove defaults.
- A custom Evaluation dimension may receive a non-zero weight only after the team defines its direction and 1, 3, and 5 scoring anchors.
- Define expected value as the magnitude and reach of the expected user or business outcome, regardless of whether it is measured in money, time, quality, or risk reduction. Its 1, 3, and 5 anchors are respectively: a marginal local improvement; a meaningful improvement for one workflow or team; and a material, measurable outcome across a priority workflow or organization.
- Define strategic alignment as how directly an Opportunity advances the Decision frame's stated goal. Its 1, 3, and 5 anchors are respectively: a weak or indirect connection; support for one stated priority; and direct advancement of the primary decision goal or a critical organizational priority.
- Define data readiness as whether the data needed for the proposed AI workflow is available, usable, permitted, and sufficiently understood. Its 1, 3, and 5 anchors are respectively: required data is missing, inaccessible, or prohibited; relevant data exists but needs cleanup, access work, or validation; and suitable data is available, permitted, and well understood.
- Define delivery ease as the relative ease of delivering the Opportunity across integration, change management, evaluation, and delivery work. Its 1, 3, and 5 anchors are respectively: major, multi-team effort with substantial dependencies or change management; moderate cross-functional delivery work; and a light, contained change with few dependencies.
- Define risk manageability as how limited, understood, and mitigable the Opportunity's legal, safety, privacy, operational, and adoption risks are. Its 1, 3, and 5 anchors are respectively: major unmitigated risks; material risks with credible mitigations; and limited, understood risks with straightforward mitigations.
- Define Evidence confidence as the strength and corroboration of the team's Evidence. Its 1, 3, and 5 anchors are respectively: mostly assumptions or anecdotes with little corroboration; some relevant qualitative or quantitative Evidence with important gaps remaining; and multiple credible, relevant sources or direct measurements supporting the Opportunity.
- Represent each Assessment as a whole-number score from 1 to 5, an optional rationale, and an Assessment confidence indicator. A score of 1 is very weak or unfavourable and 5 is very strong or favourable before applying the Evaluation dimension's direction. Assessment confidence records the evaluator's certainty in that score and does not affect Ranking; the weighted Evidence confidence dimension measures the strength of the Opportunity's Evidence. The system must preserve raw Assessments separately from calculated rank.
- Calculate a transparent weighted ranking from Assessment scores and current weights. Evaluation dimensions whose lower values are better must be normalized before aggregation. Show the factors contributing to an Opportunity's ranking in the interface.
- An Opportunity is eligible for the ranked shortlist only when it has an Assessment for every Evaluation dimension with a non-zero weight. Otherwise, show it on the portfolio board as unranked and needing assessment.
- A team may select an unranked Opportunity as its Next Opportunity decision, but the missing weighted Assessments must be conspicuous and the required rationale must explain the override.
- Equal weighted scores share the same rank and are displayed alphabetically by Opportunity title.
- Weight changes update the derived Ranking immediately while the current Iteration is a draft. Record the Decision's Ranking and weights when the team sets the Iteration; retain that snapshot within the read-only Iteration.
- Start the default Evaluation dimensions with equal weights. Display AI-proposed weights as muted initial values in the relevant fields, with each Decision-frame rationale available on hover; they do not affect the active Ranking until applied. A Team member may apply an entire suggested weight set with one action and may then edit individual weights.
- Make shared context, use cases, scores, weights, rationales, and the final shortlist editable by all team members. Use temporary field-level edit locks to prevent competing writes to the same field while allowing parallel work on other fields and Opportunities.
- Automatically persist field edits without an explicit Save action, using a 750 ms debounce. Acquire a field-level edit lock when editing begins, visibly identify its holder to other team members, release it after two minutes of inactivity, and show collaborators the latest auto-saved field value rather than each keystroke.
- Treat AI assistance as a bounded suggestion service. Before proposing candidate Opportunities, it lets the team either answer optional clarifying questions or generate drafts immediately. It may suggest structured wording, missing-context prompts for a selected Opportunity, or Evaluation-dimension weight changes from the Decision frame. Each suggestion must visibly identify generated assumptions and uncertainties, invite correction or supporting evidence, and never write portfolio data without team-member review.
- Keep the Decision frame team-authored. AI may use it as input but does not draft or rewrite its shared content.
- AI may summarize trade-offs among shortlisted Opportunities, but must not recommend or select the Next Opportunity decision.
- Ensure the interaction distinguishes AI suggestions from accepted portfolio content and supports accepting, editing, or discarding each suggestion.
- Provide a portfolio board as the primary scan-and-compare view, a detailed shaping view for an individual use case, and an evaluation/prioritization view or panel. The exact visual style is implementation-led, but it must be visibly more useful for comparison than a plain spreadsheet.
- The demonstrable live-collaboration model lets all team members edit the shared Workspace. A temporary field-level edit lock prevents concurrent edits to the same field; cursors, presence, text merging, and broader conflict resolution are not required.
- Include a realistic, neutral sample organization and six to eight opportunities so the demo can show comparison, shaping, reweighting, and selection without requiring user setup.
- Design the demo path around a complete, judge-testable flow: inspect context, compare opportunities, shape one candidate, review its evaluation rationale, adjust weights, and record a shortlist decision.
- Record the project’s use of Codex and GPT-5.6 in the README and submission materials. The public demo must show a working experience and accurately explain both uses.

## Testing Decisions

- Test external portfolio behaviour, not implementation details. A good test proves what a team member can observe: stored content, ranking results, visibility of rationale, allowed edits, and decision persistence.
- Test the portfolio-workspace boundary as the highest seam. Cover loading a draft Iteration's context and Opportunities, derived completeness, rubric edits, score updates, ranking recalculation, shortlist decision recording that sets an Iteration, not-pursuing decisions, and starting a new Iteration through its public operations.
- Test weighted ranking with representative mixtures of positive-direction and inverse-direction dimensions, 1–5 whole-number scores, zero and changed weights, and equal scores with deterministic tie handling. Test that incomplete weighted Assessments leave an Opportunity visibly unranked and ineligible for the shortlist.
- Test that weight changes alter derived ordering while leaving raw assessment data intact.
- Test that recording a Next Opportunity decision sets the Iteration read-only and retains its Ranking-and-weights snapshot.
- Test that starting a new Iteration from a set Iteration preserves the prior decision, rationale, and snapshot unchanged.
- Test that a score's rationale and confidence are returned with the relevant use case, so that ranking explanations cannot lose their evidence context.
- Test AI-assistance requests at the service boundary with controlled responses. Verify that suggestions visibly identify generated assumptions and uncertainties, are clearly presented for correction and review, and do not become persisted Opportunity content until a team member explicitly accepts or edits them.
- Test collaborative editing behaviour at the UI boundary: team members can edit unlocked fields with automatic persistence, can see the holder of a temporary lock, cannot edit fields locked by another team member, and can complete the end-to-end portfolio flow.
- Test that a Team member's chosen display name persists in their browser and identifies the field-level locks they hold.
- Add end-to-end coverage for the demo path: load seeded workspace, inspect portfolio, shape a candidate, change a weight, observe the ranking update, and save a shortlist rationale.
- There is no existing test prior art in this repository. Establish focused domain/interaction tests around the portfolio-workspace boundary and a small set of end-to-end tests around the visible workflow.

## Out of Scope

- Importing spreadsheets, documents, notes, images, or workshop artifacts.
- Tracking deployed model or agent quality, cost, latency, or human-override performance.
- AI-driven portfolio blind-spot analysis or duplicate detection beyond the team-requested candidate Opportunities generated from the Decision frame.
- Multiple saved named evaluation lenses.
- A configurable multi-axis opportunity map or advanced animated visualizations beyond what is necessary to demonstrate ranking updates.
- A future “hot session” mode that iteratively compares candidates and promotes a replacement champion.
- Simultaneous multi-user editing, presence indicators, cursors, merge/conflict handling, and fine-grained permissions.
- Full field-level edit history or version history; the MVP retains history only for explicit decision records.
- Industry-specific templates, integrations, and enterprise identity/administration.
- Building, deploying, or evaluating the selected AI solution itself; the product helps decide what to pursue.

## Further Notes

- Recommended hackathon track: **Work & Productivity**.
- The project must remain a runnable, non-trivial product. The portfolio board alone is insufficient; judges should be able to complete the full decision flow.
- The intended submission needs a public sub-three-minute YouTube demo with audio, a repository and README, and the `/feedback` Codex Session ID for the primary build thread. Consult `docs/research/openai-build-week.md` before implementation and submission planning.
- This spec synthesizes `docs/planning/ai-use-case-portfolio.md`. That note remains the record of the discovery interview and deferred ideas.
