# Opportunity Map prototype brief

Status: review checkpoint — not implementation-ready

This brief synthesizes the accepted discovery decisions from GitHub issues #6, #10, #11, #12, and #13. It supersedes conflicting prototype language until the product review is complete.

## Product model

- **North Star** is the organization’s longer-lived AI vision and strategy.
- An **Opportunity Map** is a living team space for exploring and evaluating possible AI use cases.
- An **Island** is the user-facing representation of an Opportunity. It may begin as a short team note and become richer through team discussion and optional AI help.
- **Map focus** is the specific goal, problem, or question the current Map explores. It relates Islands to the North Star.
- An **Expedition** is a first-class, team-confirmed ranking of Islands worth exploring or developing further. Confirmation preserves a snapshot of the Map, while the Map itself remains editable.

## First Map journey

1. A person enters the Workspace and chooses a plain browser-persisted display name once.
2. The team starts an Opportunity Map. It can be broad or focused on a particular workflow/user experience.
3. The Map begins fresh: no history, carry-forward review, or prior-decision empty state.
4. The team builds a free-form Opportunity Board. **Add an opportunity** is central; each Island may be a lightweight note or more developed content.
5. **Get AI suggestions** is optional. AI suggestions remain visibly distinct and are never added automatically.
6. The team prepares an Expedition from the Map’s evaluations, reviews the suggested ranking, may adjust it, and confirms the snapshot.

## Opportunity Board

The Board is an old-school atlas-map experience, not a table or plain list.

- North Star/Map focus are the conceptual compass and destination.
- Islands are possible opportunities the team may explore or develop.
- The first Board is free-form: do not require groups, columns, themes, or workflow categories.
- Support asynchronous contribution: a shared Map can collect participants’ notes before or between meetings.
- Detailed card interaction remains open for a later visual prototype pass.

## Expedition

The Expedition is a separate first-class artifact, not a terminal Map state.

- The Map’s evaluations produce a transparent suggested order.
- The team can adjust order and inspect why it changes.
- The team confirms the Expedition; no extra team-written rationale is required in the first version.
- Confirmation preserves relevant Islands and evaluation context as a historical snapshot.
- The Map continues evolving after confirmation.

## AI guide

The first built-in AI guidance appears in **Prepare Expedition**.

- Show a quiet, proactive AI briefing by default. It is expandable/dismissible and never blocks confirmation.
- Cover every Island for a small Expedition; for larger sets focus on leading Islands and meaningful outliers.
- Explain trade-offs, evidence gaps, missing ownership, absent success measures, workflow clarity, and focus versus breadth.
- Recommend concrete preparation actions for discussion, but do not create tasks or mutate Map/Expedition content without explicit team action.
- AI is advisory. It never silently reorders, confirms, or selects an Island.
- Guidance must be research-informed, inspectable, and based on validated primary sources rather than opaque doctrine.

## Later Maps

A later Map starts from a completed Map through an explicit transition:

1. Choose **Start a new map**.
2. See the previous Map focus as an immediately editable suggestion: “Keep the focus from the previous map?”
3. Review inherited Islands one at a time. **Keep** is default; Archive requires a short reason and remains restorable while the new Map is open.
4. Receive an old-atlas-style generated Map name that can be edited immediately.
5. See a short **Map ready** handoff, then enter the regular Board.

Do not require a “what changed?” note. **Map changes** should instead be a read-only comparison of Map focus, Islands, and relevant content across Maps.

## Open prototype questions

- How should opening an Island work while retaining the Board’s visual strength?
- How should a confirmed Expedition and its history be displayed as first-class destinations?
- What is the right visual form for Map changes across time?
- Which primary sources and versioning process should underpin AI guidance?
- What concrete Map-focus entry screen best captures “why now” without becoming a heavy briefing form?

## Explicitly out of scope for the first iteration

- Board grouping/columns/themes beyond the atlas-map direction.
- AI help during Map start or initial Island creation as a mandatory flow.
- Task or delivery-management features created from AI recommendations.
- AI-selected or auto-confirmed Expeditions.
