# Implementation handoff

**Updated:** 2026-07-16  
**Status:** production implementation is approved; start with GitHub issue [#15](https://github.com/nogna/opportunity-atlas/issues/15).

This is the durable entry point for a fresh Codex session. GitHub Issues are the active-work source of truth; this document is a concise orientation aid, not a replacement for the tickets.

## Start here

1. Read `AGENTS.md`, then [#15](https://github.com/nogna/opportunity-atlas/issues/15) and its linked parent [#9](https://github.com/nogna/opportunity-atlas/issues/9).
2. Read `docs/planning/opportunity-map-prototype-brief.md`. It captures approved product decisions. Where it conflicts with the older `docs/planning/ai-use-case-portfolio.md` or the current app, the prototype brief and the open production tickets win.
3. Before planning or re-scoping, read `docs/research/openai-build-week.md` and `docs/planning/ai-use-case-portfolio.md` as required by `AGENTS.md`.
4. Begin implementation with **#15 only**. Keep its GitHub conversation updated with material decisions, blockers, and status.

## Current product vocabulary and boundary

- **North Star:** the organisation's longer-lived AI vision and strategy.
- **Opportunity Map:** a living team space for exploring and evaluating AI use cases.
- **Map focus:** the specific goal, problem, or question a Map explores.
- **Island:** the visual representation of an Opportunity; it can begin as a lightweight team note.
- **Expedition:** a team-confirmed, ranked snapshot of Islands to explore or develop. It does not freeze the Map or autonomously choose a winner.

The MVP is a facilitator-led, shared browser experience. AI is advisory: it must not silently create content, reorder Islands, confirm an Expedition, or present guidance as a delivery/deployment approval.

## Approved implementation roadmap

| Issue | Deliverable | Dependency |
| --- | --- | --- |
| [#15](https://github.com/nogna/opportunity-atlas/issues/15) | First fresh Opportunity Map and atlas-style Board; editable Map focus/name; add and persist Islands | Start here |
| [#16](https://github.com/nogna/opportunity-atlas/issues/16) | Quick in-Map Island overlay; team note, optional AI formulation, Map context | #15 |
| [#17](https://github.com/nogna/opportunity-atlas/issues/17) | Explainable, adjustable ranking and confirmed Expedition snapshot | #15 |
| [#18](https://github.com/nogna/opportunity-atlas/issues/18) | Inline AI guidance and optional advisory preflight | #17 |
| [#19](https://github.com/nogna/opportunity-atlas/issues/19) | Read-only, atlas-style Expedition cabinet | #17 |
| [#20](https://github.com/nogna/opportunity-atlas/issues/20) | Later-Map carry-forward review | #15 |
| [#21](https://github.com/nogna/opportunity-atlas/issues/21) | Display name, autosave/field locks, coherent seeded judge journey, README | #15, #16, #17 |

Do not implement downstream tickets merely because they are labelled `ready-for-agent`. Work one independently actionable ticket at a time unless the user explicitly authorises parallel implementation.

## Essential first-Map constraints (#15)

- First Map begins fresh: no history, carry-forward, archive review, or prior-decision state.
- Map focus and old-atlas-style generated Map name are immediately editable.
- The Board is a free-form **old-school atlas map**. Islands must read visually as Islands, not generic cards or a plain list.
- **Add an opportunity** is the central action. An Island may start as a brief team-authored note.
- Persist the result and verify it survives reload.

## Approved interaction references

The following are throwaway prototype artifacts, not production code or a mandated architecture. Use them only to recover approved interaction intent:

- `static/prototype-opportunity-board.html` — atlas-map visual direction.
- `static/prototype-island-lab.html?variant=A` — selected lightweight in-Map Island opening.
- `static/prototype-expedition-history.html?variant=B` — selected Expedition cabinet direction.
- `static/prototype-map-journey.html` — first and later Map journey.
- `static/prototype-expedition-guide.html` — selected inline guidance with optional preflight escalation.

Do **not** ship these files, derive production state from their hard-coded markup, or treat their variants as product requirements. Their corresponding discovery/prototype issues (#6, #12, #13, #14) are closed.

## Research-backed AI guide boundary (#18)

Read `docs/research/ai-guide-expedition-evidence.md` before implementing #18. The guide should make workflow, accountable owner, baseline, outcome, evidence, and uncertainty inspectable. It distinguishes provided information, assumptions, and missing evidence; it is dismissible and does not block confirmation or create tasks.

## Current codebase and worktree warning

The current Python standard-library application (`app.py`, `workspace.py`, `ranking.py`, `collaboration.py`, and `static/`) implements the **superseded Iteration/Shortlist/Decision Frame model**. Reuse only well-tested technical foundations where they fit; do not preserve old user-facing concepts merely because they are in code or the README.

The working tree is intentionally dirty and contains both earlier implementation changes and prototype/research files. In particular, `app.py`, `README.md`, `static/iteration.*`, `static/styles.css`, `test_app.py`, `CONTEXT.md`, `AGENTS.md`, `.scratch/ai-use-case-portfolio/spec.md`, `data/`, and the prototype files have uncommitted changes. Inspect and deliberately include, replace, or leave each change—never use `reset --hard`, blanket checkout, or assume the worktree is disposable.

## Validation, review, and publication checklist

For each implementation ticket:

1. Fetch/read its GitHub Issue and linked decisions; add a status comment before substantial independent work if needed.
2. Build at an intentional seam and add/adjust focused tests first where practical.
3. Run focused tests regularly and the complete suite at the end: `python3 -m unittest -v` (the app uses the standard library only). Run the local server with `python3 app.py` and manually test the relevant browser flow and reload persistence.
4. Update the ticket with material decisions, validation evidence, dependencies, and completion status. Close it only when its acceptance criteria are met.
5. Use the repository `code-review` skill after implementation, as required by the `implement` skill. Address findings or record why they do not apply.
6. Review `git diff` and `git status`; stage only the intended files. Commit on the current branch with an issue-linked, focused message. Do not commit throwaway prototypes unless the user explicitly wants them retained.
7. Push only after explicit user approval for that exact push. Report the commit hash, tests, and ticket state.

## Hackathon guardrails

The target is **Work & Productivity**. The project must be runnable, use Codex and GPT-5.6, and have a coherent demo—not just a static prototype. Before submission, re-check the official Build Week rules; the stored planning note says the deadline is 2026-07-22 02:00 CEST and lists required README, demo-video, repo, testing, and `/feedback` session materials.
