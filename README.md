# Opportunity Atlas

Opportunity Atlas is a Python web app for discovering, shaping, evaluating, and prioritizing AI use cases as a shared decision artifact.

**Track:** Work & Productivity. It helps a team turn a pile of AI ideas into one evidence-backed next opportunity to pursue, without a spreadsheet or a black-box ranking.

## Run locally

The app uses only the Python standard library.

```sh
python3 app.py
```

Open <http://localhost:8000>. Set `PORT` to use a different port. Set `OPENAI_API_KEY` to enable live AI assistance; without it, a local guidance fallback keeps the demo runnable.

Run the focused domain tests with:

```sh
python3 -m unittest -v
```

## Demo path

The app opens a seeded Workspace, so this path needs no account or data entry:

1. Check the **North Star** destination: the Workspace's AI vision (its enduring centre inscription) and AI strategy (its plotted course of current priorities). It is shared across the whole Workspace.
1. Start on the living **Map**. Each Island is an AI opportunity.
    * _If you dont want to charter an **Island** when you create it you can just add a personal **Scouting note** on the map, then explicitly chart it as an Island when the team is ready._
1. Click on an **Island** on the map to use its **Chart Room**. There you can  capture the current workflow, possible AI-enabled change, outcome, team evidence, unknowns, and explained evaluation values. 
1. Open **Expedition**, set a planning horizon and set how the different demensions should be weighted. Once you have set the weights, show the **Islands** rankings, select what islands you want included in the **Expedition**
1. The Map is a living enitiy can while the **Expedition** is ongoing more **Islands** can pop up as well as **Scouting notes**. **Compare Map changes** later to see added Notes and Islands, changed values, and any new unselected Island that now outranks a selected one.


To reset a locally changed demo Workspace, stop the server and remove `data/workspace.json`; the next launch recreates the seed.

## OpenAI and Codex

### In development
I used codex with gpt-5.6 throughout development and in combination with Matt Pollcock skills to help me navigate my own thoughts and ideas to a more clear product. As I have not used codex previously nor Matt skills I thought it was a really good exercise to work in this way. Both the prototyping and agent interace was really sweet and helped a lot when doing design descions. When my Codex tokens ran out near the deadline, I switched to Claude Code for the remaining submission-polish work.

### In app
The app’s AI assistance is intentionally review-first: it helps articulate an AI use case and surface missing context. It should be the human(s) in charge and get guidance and help from the AI. The implementation uses the OpenAI Responses API and `gpt-5.6` when an API key is available; without one, a labelled local guidance fallback keeps the demo runnable.

## Hackathon submission

`/feedback` Codex Session ID for the Project thread where the majority of core functionality was built: `019f61c5-f40d-7492-8174-4416884001e6`

### For models developing
See `docs/research/openai-build-week.md` for the remaining hackathon submission requirements.