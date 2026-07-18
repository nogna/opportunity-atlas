# Opportunity Atlas domain glossary

## Workspace

A separate shared home for one team or clearly distinct area. A Workspace provides that team's North Star and contains its living Opportunity Map. Different teams or substantially different areas use separate Workspaces.

## Opportunity Map

The living atlas for one team's or area's AI opportunities. It evolves as Islands are discovered, developed, or archived. A Map never becomes read-only. Its name describes the team or area it serves, rather than an iteration or generated milestone name.

## Map snapshot

An immutable record of how an Opportunity Map looked when an Expedition was confirmed. It lets people see that the current Map has since changed, without locking or replacing the Map.

## North Star

A first-class, old-atlas Workspace entity. Its **AI vision** is the enduring centre inscription: the long-lived direction and principles for how AI should contribute. Its **AI strategy** is the plotted course: current priorities, concrete goals, focus areas, and guardrails. Maps do not duplicate it; AI uses it as a compass to help formulate Islands toward the stated goals and strategy, never as a gate that rejects exploratory work. When either part is missing, the product makes that visible and offers a non-blocking setup action.

## Island

The user-facing, old-atlas representation of one AI opportunity on an Opportunity Map. A team may create an Island directly or transfer a Scouting note into one. When a note is transferred, the Island preserves it as provenance. The Island's Chart Room is the team's deep-dive workspace for developing a credible opportunity hypothesis and its evaluation values. AI can guide that work, but the team decides what becomes team-authored Island content.

## Scouting note

A lightweight, individually authored pre-meeting contribution for a possible Island. A Team member can add it before Expedition planning to surface an early observation, idea, or prompt to explore. It does not yet claim to be an opportunity on the Map. The team may later transfer it into an Island; the transferred Island preserves the note as visible provenance while its development happens in the Island-development workspace.

## Chart Room

The team-visible, old-atlas deep-dive workspace for an Island. It keeps observations, supporting or challenging evidence, AI lenses, assumptions, and unanswered questions distinct while the team develops the Island's opportunity hypothesis and adjustable evaluation values. Contextual guided help is available within the Chart Room. AI may help organise or question this material but cannot transfer a Scouting note, author team content, or alter evaluation values. “Evidence board” and “Island-development workspace” are superseded user-facing names.

## Archived Island

An Island the team has removed from the active Map because it no longer belongs. Archiving requires a short reason and is reversible. Archived Islands remain available through an optional archived-Islands view.

## Expedition

A first-class, team-confirmed, evidence-seeking commitment to the one Island the team will explore next, unless it explicitly chooses a broader commitment during Expedition planning. Its intent is expressed through an Island Charter for each included Island. An Expedition has a required planning horizon and an explainable, time-bound **Expedition lens**: it applies weights to existing Island values using that horizon and the Workspace strategy to suggest a focus order. The team can adjust the lens and final order; an override reason is recorded when the final order differs. An Expedition is sprint-like in intent but has no fixed duration; its intended Island count is chosen for each planning session and defaults to one. Only one Expedition is active on a Map at a time; starting another makes the prior one past.

## Expedition planning

The pre-confirmation Map activity where the team states its intended number of Islands, planning horizon, and weighting lens, then receives a suggested top set and focus order. It is not a separate durable artifact: it leads into the confirmed Expedition and its Island Charters.

## Expedition lens

The time-bound weighting of existing Island evaluation categories for one Expedition. AI may propose initial weights from the planning horizon and Workspace strategy, with a visible explanation. The team owns every weight and the resulting focus order. Its snapshot preserves the horizon, weights, Island values used, suggested order, final order, and any override reason.

## Island Charter

A compact, Expedition-specific plan for one selected Island. It expresses what the team intends to learn or do next for that Island and may capture an intended outcome, participants, or decision evidence. It is time-specific to the Expedition and does not replace the durable opportunity hypothesis, evidence, or evaluation values held in the Island's Chart Room.

## Opportunity hypothesis

The concise link assembled while developing a Scouting note: today's way of working or problem, an AI-enabled change, and a possible outcome. It helps the team test whether changing the workflow—not merely deploying a tool—could create value. A promoted Island retains this hypothesis.

## Value evidence

The practical signal attached to an Island that can help the team learn whether its opportunity hypothesis is working. It may be a measurable result or an observable outcome; it is not required to be a formal ROI calculation.

## Map changes

A read-only comparison between an Expedition's Map snapshot and the current living Map. It distinguishes newly added personal Scouting notes from newly charted Islands, makes changed Island evaluation values legible as previous and current numbers, and makes archived Islands visible without requiring a change note or manual Map versions. When current Map values newly make an unselected Island stronger than a selected Expedition Island, it shows a calm notice; the notice does not re-rank, alter, or replace the Expedition.

## AI suggestion

Transparent, optional help that can formulate an Island, propose alternative AI-enabled approaches, identify missing context, or challenge weak assumptions and trade-offs. It ties its advice to the Workspace North Star and visibly distinguishes team-provided information, assumptions, and suggestions. It remains distinct from team-authored content and never changes Island values, selects Islands, confirms an Expedition, or archives an Island without explicit team action.

## Evidence

Team-authored notes and optional links that support or challenge an Island or its evaluation values. AI may structure or question Evidence but does not present generated claims or citations as team Evidence.

## Evaluation value

A visible, adjustable input on an Island that helps the team compare opportunities. Evaluation values are authored on Islands in the Map; Expedition does not introduce a separate ranking model.

## Team member

A person collaborating in a shared Workspace. A Team member chooses a display name when opening the Workspace; the name identifies temporary edit locks.

## Field-level edit lock

A temporary claim on one editable Map or Island field. While a Team member edits that field, others cannot edit the same field but can continue working elsewhere.

## Legacy terms

**Iteration**, **Decision frame**, **Map focus**, **Shortlist**, **Next Opportunity decision**, and **not-pursuing decision** are superseded product language. Do not introduce them in new user-facing work. **Pilot** should not describe an Expedition unless the team deliberately uses it for a specific next action.
