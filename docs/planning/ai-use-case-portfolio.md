# AI Use-Case Portfolio

## Purpose

Create a living, shareable decision artifact that helps an AI team, its stakeholders, and cross-functional partners discover, evaluate, and prioritize AI use cases. It is the glue between people who can build AI systems and people who need to decide what outcomes to pursue.

The product should replace a spreadsheet as the center of the conversation. It should make the team’s context, assumptions, trade-offs, and decisions easy to see and discuss.

## Core user outcome

After using the workspace, a group can identify and agree on an evidence-backed next AI use case to pursue.

## Product principles

- The team owns strategic judgement; AI assists rather than acting as an opaque decision-maker.
- Context and evaluation rationale must be explicit, inspectable, and comparable across use cases.
- The artifact persists beyond a workshop and can be shared with stakeholders.
- Start with best-practice AI-use-case evaluation dimensions, but let teams configure and reweight them.
- A use case becomes more detailed only after it survives early screening.

## Agreed MVP

### 1. Shared context

The workspace contains a short, structured team/organization context shared by all use cases. Initially this is entered manually. It may include strategic goals, key user groups, workflows, constraints, and available data.

### 2. Opportunity portfolio board

The home screen is a table/board for scanning many AI opportunities. It is more expressive than a spreadsheet, but preserves the practical ability to compare, sort, and inspect a portfolio.

Each opportunity should expose its stage, context, evidence, and evaluation inputs at a glance. A richer detail view opens for an individual opportunity.

### 3. AI-assisted use-case shaping

For a shortlisted opportunity, AI helps the user make the entry clear and complete. It can draft and refine the problem, target user, outcome, proposed AI role, missing context, and evaluation rationale.

AI should not make an opaque strategic decision for the group.

The deeper shaping view describes the transformation:

```text
Current workflow / pain → proposed AI-enabled workflow → expected outcome
```

This happens after shortlisting, not for every initial candidate.

### 4. Configurable evaluation

Use cases are evaluated against a best-practice default rubric. The exact dimensions, labels, and weights are configurable live by the team.

Suggested default dimensions:

- Expected value
- Strategic alignment
- Data readiness
- Delivery effort
- Risk
- Confidence in the evidence

The system must make the resulting ranking explainable from the underlying fields and weights.

### 5. Shortlist and living artifact

Changing weights updates the prioritization of the portfolio. The team can shortlist the next opportunity to pursue and retain the rationale as part of the persistent artifact.

### 6. Collaboration boundary

For the MVP, use a facilitator-led live session: one person makes edits while viewers see saved/live changes. Full simultaneous editing is out of scope.

## Agreed end-to-end flow

```text
Shared context
  → opportunity portfolio board
  → AI-assisted use-case shaping
  → configurable best-practice evaluation dimensions
  → live weights and ranked shortlist
  → persistent, shareable decision artifact
```

## Deferred ideas

These are valuable follow-ons, not MVP requirements:

- Import existing documents, spreadsheets, images, notes, or workshop outputs.
- Track real model/agent performance after a use case becomes an implementation initiative.
- AI-assisted portfolio blind-spot discovery: identify duplicates, missing workflow areas, weak assumptions, or alternative opportunity clusters.
- Multiple saved named evaluation lenses, such as "quick wins" and "strategic bets".
- Advanced visualizations, including a two-axis opportunity map with animated changes as weights change.
- Full real-time collaborative editing, presence, cursors, and conflict handling.
- Domain-specific templates and imported evidence sources.

## Hackathon fit

Recommended track: **Work & Productivity**.

The demo should show a believable portfolio of several opportunities moving through discovery, evaluation, and shortlisting. It must demonstrate a complete working experience, not only a static visualization. See `docs/research/openai-build-week.md` for current official submission requirements, including the need to show how Codex and GPT-5.6 were used.

## Open choices for later planning

- A name and visual identity for the product.
- The sample organization/domain and the 6–8 demo opportunities.
- Exact default-rubric definitions and scoring scales.
- Which visuals are necessary for the initial demo beyond the board and ranked shortlist.
- Data model, Python web framework, frontend approach, authentication, and deployment approach.
