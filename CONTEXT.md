# Opportunity Atlas domain glossary

## Workspace

The single shared, persisted portfolio used by a team to compare AI use cases, adjust their evaluation rubric, and record its next bet through ordered Iterations. All team members who open the MVP can edit its current Iteration; prior Iterations are read-only history. The MVP has exactly one Workspace; workspace creation, selection, and tenant separation are out of scope.

## Iteration

One long-lived, editable draft of the decision artifact, containing the Decision frame, Opportunities, Evaluation dimensions, weights, Assessments, Shortlist, and Archive decisions for an exploratory or evaluation cycle. It has an automatic sequential name and may have a custom name, which is editable only while the Iteration is a draft. An Iteration becomes set and read-only only when the team records one Next Opportunity decision. If no candidate is suitable, it remains a draft while the team records not-pursuing decisions or continues exploration. A new Iteration begins with a carry-forward review that records which inherited Opportunities to keep or archive, then copies the kept content as its editable starting point and records what changed. Iterations form one linear sequence, and their lineage prominently identifies the source Iteration, creation time, and reassessment trigger.

## Decision frame

The shared, evolving context for a Workspace: its strategic goal, target users, workflows, constraints, available data, and decision to make. It can begin broad or narrow; unknown fields do not block the team from adding Opportunities.

## AI suggestion

Proposed Opportunity wording, missing-context prompts, candidate Opportunities, Evaluation-dimension weight changes, trade-off summaries, or carry-forward review flags generated from the Decision frame. An AI suggestion visibly identifies its assumptions and uncertainties, is distinct from team-authored content, and never becomes Workspace content until a Team member explicitly adds, accepts, or edits it; it does not recommend or select a Next Opportunity decision or archive an Opportunity.

## Evidence

Team-authored notes and optional links that support or challenge an Opportunity or Assessment. AI may structure or question Evidence but does not claim external research or generate citations as Evidence in the MVP.

## Opportunity

One candidate AI use case within a Workspace. An Opportunity captures the affected user and workflow, the current pain, the proposed AI-enabled workflow, expected outcome, Evidence, and Assessments; its maturity is derived from this content rather than a lifecycle stage.

## Not-pursuing decision

A recorded decision to set an Opportunity aside, including its rationale, the Team member who recorded it, and its timestamp. It is reversible while its Iteration is a draft; once the Iteration is set, reconsideration belongs in a new Iteration.

## Archive decision

A record in a new Iteration that an inherited Opportunity is no longer relevant to that Iteration, including its reason and a compact read-only summary linking to the source Iteration. The Opportunity remains available in the source Iteration's history and may be restored while the new Iteration is a draft.

## Shortlist

A manually curated set of promising Opportunities selected for focused comparison. It is distinct from the one recorded next Opportunity to pursue.

## Next Opportunity decision

The recorded selection of one Opportunity from an Iteration's Shortlist as the next one to pursue, including its rationale, recording Team member, timestamp, and a snapshot of the Ranking and weights when it was made. Recording this decision sets the Iteration as read-only; later reassessment belongs in a new Iteration.

## Evaluation dimension

One configurable criterion used to compare Opportunities, such as expected value or delivery effort. It has a direction that determines whether a higher or lower Assessment score is favourable; every default Evaluation dimension includes a concise definition and 1, 3, and 5 scoring anchors.

## Assessment

An Opportunity's evidence-backed evaluation against one Evaluation dimension. An Assessment has a whole-number score from 1 to 5, an optional rationale, and an Assessment confidence indicator; the indicator reports the evaluator's certainty in that score and does not affect Ranking.

## Evidence confidence

An Evaluation dimension that measures the strength of an Opportunity's Evidence. Unlike Assessment confidence, its score is weighted into the Ranking.

## Ranking

The derived, explainable ordering of Opportunities from their weighted Assessments. An Opportunity is unranked when it lacks an Assessment for any Evaluation dimension with a non-zero weight; equal scores share a rank and are displayed alphabetically by title.

## Team member

A person collaborating in the shared Workspace. A Team member chooses a display name when opening the Workspace; this name identifies their field-level edit locks.

## Field-level edit lock

A temporary claim on one editable Opportunity or Workspace field. While a team member edits a field, other team members cannot edit that same field, but can continue working on other fields and Opportunities.
