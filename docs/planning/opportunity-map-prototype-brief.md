# Opportunity Map product brief

Status: current product model

## Core model

- A **Workspace** is for one team or distinct area and carries its first-class North Star. In the old-atlas theme, AI vision is its enduring centre inscription; AI strategy is its plotted course of current priorities, goals, focus areas, and guardrails.
- An **Opportunity Map** is that team's living atlas. It is named for the team or area, never becomes read-only, and evolves as Islands are discovered, changed, or archived.
- A **Scouting note** is a lightweight, individually authored pre-meeting contribution for a possible Island. It is not yet an opportunity on the Map, but may later be transferred into one; the resulting Island preserves the note as visible provenance.
- An **Island** is an AI opportunity. Teams can create an Island directly or transfer a Scouting note into it. The **Chart Room** is its deep-dive space: its opportunity hypothesis, supporting or challenging evidence, assumptions, unknowns, and visible evaluation values are developed there. It is one vertically scrolling workspace, not a tabbed form. Optional, contextual AI guidance appears in an AI sidecar and may offer a more guided setup without taking authorship. “Evidence board” and “Island-development workspace” are superseded user-facing names.
- An **Expedition** is a first-class destination beside the Map. It is the team's focused, evidence-seeking commitment to one prepared Island by default. Its intent is expressed through an **Island Charter** for each included Island, rather than a generic Expedition mission. In **Expedition planning**, a required planning horizon and an explainable, time-bound **Expedition lens** apply the evaluation values already configured on Islands and the Workspace strategy to produce a paginated ranked shortlist: show the top five first and let the team continue through the rest. The top Island starts selected; the team may add more to a selected set, then explicitly continue to create Charters for that set. A horizon, lens, or Map change never silently removes a selected Island; a new top-ranked Island is clearly surfaced. A separate AI-influence control adjusts how strongly the AI Compass proposal affects the team-controlled category emphasis and suggestion. The team can adjust the lens or final order, with a recorded reason for an override. It does not repeat Island discovery or evaluation. It is sprint-like in intent but has no fixed duration.
- Confirming an Expedition saves an immutable **Map snapshot**. The Map remains editable. When the Map later differs, the Expedition shows a calm comparison with the current Map: newly added personal Scouting notes are distinct from newly charted Islands, Island values show previous and current numbers, and a new cross-over where an unselected Island becomes stronger than a selected Island is a notice only—not an automatic re-ranking or Expedition change.
- Only one Expedition is active per Map. Starting a new Expedition makes the prior one past.

## Map and Expedition journeys

1. Before Expedition planning, individual Team members may capture lightweight Scouting notes, or the team may create an Island directly. A note can later be transferred into an Island, where it remains visible as provenance rather than being discarded.
2. The Chart Room explicitly separates team observations, AI lenses, assumptions, and missing evidence. Contextual guided help within it helps the team connect the workflow or problem, an AI-enabled change, and a possible outcome. It also holds the Island's adjustable evaluation values. AI does not transfer notes, author team content, or change values.
3. The Map is where Island values are edited and Islands can be archived with a short, required reason. Archived Islands are restorable and available from an optional archive view.
4. The team enters **Expedition planning**, sets the horizon and lens, and receives a ranked shortlist. The top Island is selected by default; the team may add more before creating or reviewing a compact Island Charter for each selected Island. It may surface the selected Islands' prepared hypotheses and gaps, but does not ask the team to restate them. The confirmed Expedition presents a summary of those Charters rather than requiring a generic mission.

The selected UI direction presents this journey with a compact rail: set the lens, choose Islands, then complete Charter details. The rail makes the flow legible without turning the vertically scrolling content into tabs or blocking exploration.
5. The confirmed Expedition retains its Map snapshot. The live Map may continue changing; comparison explains how it moved on. It keeps personal Scouting notes distinct from Islands, shows changed evaluation values as previous → current numbers, and calmly flags a newly stronger unselected Island without changing the Expedition.

## Explicitly retired

- Iteration lifecycle and read-only Maps
- Start-a-new-Map carry-forward review for ordinary reprioritisation
- Map focus as a primary product field
- Shortlist and Next Opportunity decision
- The earlier ban on an Expedition ranking model is superseded: an explainable, team-controlled Expedition lens now weights existing Island values for a time-bound focus order.
- Mandatory “what changed?” notes

## Product boundary

Different teams or completely different areas use separate Workspaces. A new Expedition—not a new Map—handles the ordinary next focus for the same Map.

## North Star context

The North Star belongs to the Workspace, not a particular Map or Expedition. A Map uses it to help the team formulate Islands toward the AI vision, current strategy, and goals; it does not copy or redefine it. If the AI vision or strategy is missing, the Map shows a transparent, non-blocking warning and a setup action. A richer guided creation experience is deferred, but the entity and its missing state are first-class in the MVP.

## AI guidance

AI guidance primarily helps the team shape an Island in the Chart Room: formulate the opportunity, offer alternative AI-enabled approaches, expose missing workflow, ownership, baseline, outcome, or evidence context, and challenge weak assumptions. Its advice ties back to the Workspace North Star and distinguishes team-provided information, assumptions, and suggestions. During Expedition preparation, AI may help the team connect selected Islands and Charters to the same strategy and identify preparation gaps; it does not create a second discovery form. It never alters Island values, promotes a note, selects Islands, creates tasks, or confirms an Expedition without explicit team action.
