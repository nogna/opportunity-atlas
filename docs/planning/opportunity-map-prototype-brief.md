# Opportunity Map product brief

Status: current product model

## Core model

- A **Workspace** is for one team or distinct area and carries its North Star.
- An **Opportunity Map** is that team's living atlas. It is named for the team or area, never becomes read-only, and evolves as Islands are discovered, changed, or archived.
- A **Scouting note** is a lightweight team-authored placeholder for a possible Island. It is not yet an opportunity on the Map.
- An **Island** is a prepared AI opportunity. The team promotes a Scouting note only after developing it through an Evidence board and opportunity hypothesis. Its visible evaluation values are authored on the Island in the Map.
- An **Expedition** is a first-class destination beside the Map. It is the team's focused, evidence-seeking commitment: selected prepared Islands, a required short goal, and an optional intended outcome. It does not repeat Island discovery or evaluation. It is sprint-like in intent but has no fixed duration or size.
- Confirming an Expedition saves an immutable **Map snapshot**. The Map remains editable. When the Map later differs, the Expedition shows a calm comparison with the current Map.
- Only one Expedition is active per Map. Starting a new Expedition makes the prior one past.

## Map and Expedition journeys

1. A team enters its Map, sees North Star context, and captures lightweight Scouting notes. AI helps the team develop a note through an Evidence board, explicitly separating team observations, AI lenses, assumptions, and missing evidence.
2. The team uses a guided opportunity-hypothesis step to connect the workflow or problem, an AI-enabled change, and a possible outcome. The team—not AI—promotes a sufficiently explored Scouting note into an Island.
3. The Map is where Island values are edited and Islands can be archived with a short, required reason. Archived Islands are restorable and available from an optional archive view.
4. The team enters the Expedition destination, compares existing Island values, selects its focused Islands, states the required goal, optionally adds an intended outcome, and confirms. It may surface the selected Islands' prepared hypotheses and gaps, but does not ask the team to restate them.
5. The confirmed Expedition retains its Map snapshot. The live Map may continue changing; comparison explains how it moved on.

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

AI guidance primarily appears while developing a Scouting note toward an Island. It is advisory: identify workflow, ownership, baseline, outcome, and evidence gaps; distinguish provided information, assumptions, and missing evidence; and never alter Island values, promote a note, select Islands, create tasks, or confirm an Expedition. Expedition may surface existing Island gaps, but is not a second discovery form.
