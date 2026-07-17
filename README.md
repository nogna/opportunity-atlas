# Opportunity Atlas

Opportunity Atlas is a Python web app for discovering, shaping, evaluating, and prioritizing AI use cases as a shared decision artifact.

## Run locally

The app uses only the Python standard library.

```sh
python3 app.py
```

Open <http://localhost:8000>.

Run the focused domain tests with:

```sh
python3 -m unittest -v
```

## Demo path

The app opens a seeded Workspace, so this path needs no account or data entry:

1. Start on the living **Map**. Its North Star provides the strategic context; each Island is an AI opportunity with visible value, readiness, and effort.
2. Open an **Island** and use its **Chart Room** to capture the current workflow, possible AI-enabled change, outcome, team evidence, unknowns, and explained evaluation values. The AI Compass is guidance only.
3. Optionally add a personal **Scouting note**, then explicitly chart it as an Island when the team is ready.
4. Open **Expedition**, select prepared Islands, and give each an **Island Charter** with its next learning action. Confirming it saves a Map snapshot.
5. Keep the Map living. **Compare Map changes** later to see added Notes and Islands, changed values, and any new unselected Island that now outranks a selected one. The Expedition is never changed automatically.

To reset a locally changed demo Workspace, stop the server and remove `data/workspace.json`; the next launch recreates the seed.

## OpenAI and Codex

The app’s AI assistance is intentionally review-first: it helps articulate an AI use case and surface missing context, but never writes team evidence, evaluation values, or Expedition choices without explicit team action. The implementation uses the OpenAI Responses API and `gpt-5.6` when an API key is available; without one, a labelled local guidance fallback keeps the demo runnable. Codex was used to research, design, prototype, implement, test, and review the application.

See `docs/research/openai-build-week.md` for the remaining hackathon submission requirements.
