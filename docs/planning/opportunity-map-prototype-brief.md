# Opportunity Map product brief

Status: current product model

## Core model

- A **Workspace** is for one team or distinct area and carries its North Star.
- An **Opportunity Map** is that team's living atlas. It is named for the team or area, never becomes read-only, and evolves as Islands are discovered, changed, or archived.
- A **Scouting note** is a lightweight, individually authored pre-meeting contribution for a possible Island. It is not yet an opportunity on the Map, but may later be transferred into one; the resulting Island preserves the note as visible provenance.
- An **Island** is an AI opportunity. Teams can create an Island directly or transfer a Scouting note into it. The **Chart Room** is its deep-dive space: its opportunity hypothesis, supporting or challenging evidence, assumptions, unknowns, and visible evaluation values are developed there. It is one vertically scrolling workspace, not a tabbed form. Optional, contextual AI guidance appears in an AI sidecar and may offer a more guided setup without taking authorship. “Evidence board” and “Island-development workspace” are superseded user-facing names.
- An **Expedition** is a first-class destination beside the Map. It is the team's focused, evidence-seeking collection of selected prepared Islands. Its intent is expressed through an **Island Charter** for each selected Island, rather than a generic Expedition mission. It does not repeat Island discovery or evaluation. It is sprint-like in intent but has no fixed duration or size.
- Confirming an Expedition saves an immutable **Map snapshot**. The Map remains editable. When the Map later differs, the Expedition shows a calm comparison with the current Map: newly added personal Scouting notes are distinct from newly charted Islands, Island values show previous and current numbers, and a new cross-over where an unselected Island becomes stronger than a selected Island is a notice only—not an automatic re-ranking or Expedition change.
- Only one Expedition is active per Map. Starting a new Expedition makes the prior one past.

## Map and Expedition journeys

1. Before Expedition planning, individual Team members may capture lightweight Scouting notes, or the team may create an Island directly. A note can later be transferred into an Island, where it remains visible as provenance rather than being discarded.
2. The Chart Room explicitly separates team observations, AI lenses, assumptions, and missing evidence. Contextual guided help within it helps the team connect the workflow or problem, an AI-enabled change, and a possible outcome. It also holds the Island's adjustable evaluation values. AI does not transfer notes, author team content, or change values.
3. The Map is where Island values are edited and Islands can be archived with a short, required reason. Archived Islands are restorable and available from an optional archive view.
4. The team enters the Expedition destination, compares existing Island values, selects its focused Islands, and creates or reviews a compact Island Charter for each one. It may surface the selected Islands' prepared hypotheses and gaps, but does not ask the team to restate them. The Expedition presents a summary of those Charters rather than requiring a generic mission.
5. The confirmed Expedition retains its Map snapshot. The live Map may continue changing; comparison explains how it moved on. It keeps personal Scouting notes distinct from Islands, shows changed evaluation values as previous → current numbers, and calmly flags a newly stronger unselected Island without changing the Expedition.

## Explicitly retired

- Iteration lifecycle and read-only Maps
- Start-a-new-Map carry-forward review for ordinary reprioritisation
- Map focus as a primary product field
- Shortlist and Next Opportunity decision
- A separate Expedition ranking model
- Mandatory “what changed?” notes

## Product boundary

Different teams or completely different areas use separate Workspaces. A new Expedition—not a new Map—handles the ordinary next focus for the same Map.

## AI guidance

AI guidance primarily helps the team shape an Island in the Chart Room: formulate the opportunity beside the workflow card, offer alternative AI-enabled approaches beside the possible change card, and challenge weak assumptions beside evidence and unknowns. Responses are read-only AI-owned material: alternatives and challenges are plain bullets that can be individually added to the related team field, while a formulation can be explicitly adopted with “Use this instead.” It never automatically changes a team field. It keeps the Workspace North Star in view as a compass—not a gate—by suggesting useful alignment or surfacing a tension without rejecting exploratory work. It distinguishes team-provided information, assumptions, and suggestions. During Expedition preparation, AI may help the team connect selected Islands and Charters to the same strategy and identify preparation gaps; it does not create a second discovery form. It never alters Island values, promotes a note, selects Islands, creates tasks, or confirms an Expedition without explicit team action.
