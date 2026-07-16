## Agent skills

### Issue tracker

GitHub Issues are the source of truth for active work; `.scratch/` holds supporting specs and research only. See `docs/agents/issue-tracker.md`.

Keep the GitHub issue tracker current throughout every workflow: create and link a discovery, research, grilling, prototype, or implementation issue before starting independently actionable work; apply the canonical triage label and relevant type labels when creating or materially changing an issue; record material decisions and dependency/status changes in its conversation; and close it only after its acceptance criteria are complete. Do not advance from discovery/prototype work to implementation without an explicit user decision recorded in the relevant issue.

### Triage labels

Uses the default canonical triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

Uses a single-context domain-doc layout. See `docs/agents/domain.md`.

When the user confirms a domain or product decision, update `CONTEXT.md` and every affected canonical planning/ADR document in that same turn. Mark superseded documents explicitly; never leave conflicting product language as if it were current.

### Hackathon constraints

Before planning or scoping this project, read `docs/research/openai-build-week.md`. It records the current official OpenAI Build Week requirements, deadlines, judging criteria, and a planner checklist.

### Product direction

Before planning or scoping the product, read `docs/planning/ai-use-case-portfolio.md`. It records the agreed MVP boundary, product intent, and deferred ideas from the discovery interview.
