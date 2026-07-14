# Opportunity Atlas

Opportunity Atlas is a Python web app for discovering, shaping, evaluating, and prioritizing AI use cases as a shared decision artifact.

## Run locally

The app uses only the Python standard library.

```powershell
C:\Users\albin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe app.py
```

Open <http://localhost:8000>.

Run the focused domain tests with:

```powershell
C:\Users\albin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest -v
```

## Demo path

1. Read the shared context.
2. Compare the seeded opportunities and change a rubric weight.
3. Open an opportunity and shape its before/after workflow.
4. Use **Suggest improvements**. With `OPENAI_API_KEY` set, this calls the OpenAI Responses API using `gpt-5.6`; without a key, a local guidance fallback keeps the demo runnable.
5. Save the use case and record the next bet with its rationale.

## OpenAI and Codex

The app’s AI assistance is intentionally review-first: it drafts clearer language and exposes missing context, but never writes portfolio data without a facilitator saving it. The implementation uses the OpenAI Responses API and the `gpt-5.6` model when an API key is available. Codex was used to design, implement, and test the application.

See `docs/research/openai-build-week.md` for the remaining hackathon submission requirements.
