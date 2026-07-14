# OpenAI Build Week — planning constraints

**Status:** submissions open (as retrieved)  
**Official event page:** <https://openai.devpost.com/>  
**Official rules:** <https://openai.devpost.com/rules>  
**Retrieved:** 2026-07-13 17:33 UTC from the connected Devpost Hackathons service. The official rules and event site control if this document conflicts with them.

Use this as the constraint reference before proposing project scope, milestones, or a submission plan. It is a snapshot, not a substitute for re-checking the official rules just before submission.

## Executive constraint summary

- Build a working project that uses **Codex and GPT-5.6**, and choose exactly one of four tracks: Apps for Your Life, Work & Productivity, Developer Tools, or Education.
- The official submission window is **July 13, 2026 9:00 AM–July 21, 2026 5:00 PM Pacific Time**. In Stockholm (CEST), the hard deadline is **July 22, 2026 02:00**.
- The submission needs a public YouTube demo under three minutes with audio explaining the build and how both Codex and GPT-5.6 were used; a repo URL; a README; and the `/feedback` Codex Session ID for the thread where most core work was done.
- Plan an actually runnable, non-trivial product—not a proof of concept—and make it easy for judges to test without rebuilding. The four judging criteria are equally weighted.
- If extending an existing project, isolate and document the new hackathon-period work and evidence of Codex/GPT-5.6 usage.

## Official rules — verbatim excerpts

The following are deliberately quoted from the formal rules returned by Devpost. They are the most important hard requirements; read the [full official rules](https://openai.devpost.com/rules) for complete terms.

> “Projects must be either newly created during the Hackathon Submission Period or, if the Project existed prior to the Submission Period, must have been meaningfully extended using Codex and/or GPT-5.6 after the Submission Period start date.”

> “The Project must be capable of being successfully installed and running consistently on the platform for which it is intended and must function as depicted in the video and/or expressed in the text description.”

> “The video portion of the Submission: should be less than three (3) minutes. Judges are not required to watch beyond three minutes[;] must include a clear demo with audio that covers what you built and how you used Codex and GPT-5.6[; and] must be uploaded to and made publicly visible on YouTube.”

> “Provide /feedback Codex Session ID for your Project thread where the majority of core functionality was built.”

> “The Entrant must make the Project available free of charge and without any restriction, for testing, evaluation and use by the Sponsor, Administrator and Judges until the Judging Period ends.”

> “All Submission materials must be in English or, if not in English, the Entrant must provide an English translation of the demonstration video, text description, and testing instructions as well as all other materials submitted.”

## Eligibility and ownership

**Verbatim eligibility summary from Devpost:**

> “Above legal age of majority in country of residence”

The official rules also permit eligible individuals, teams, and eligible organizations. Teams/organizations need an authorized representative; one eligible person may participate individually and in more than one team or organization. The rules exclude, among others, people/organizations outside the listed supported countries, people in prohibited jurisdictions (examples expressly include Brazil, Quebec, Russia, Crimea, Cuba, Iran, North Korea, and Syria), promotion entities and their close family/household, judges/employers of judges, and conflicts of interest. Verify the current [supported-country list](https://platform.openai.com/docs/supported-countries) and the full rules for edge cases.

Submission IP must be original, solely owned by the entrant/team/organization, and not infringe others’ rights. Third-party SDKs, APIs, and data require authorization. Open source is allowed when its licence is followed and the submission meaningfully enhances the underlying project. A project developed with financial or preferential support from OpenAI or Devpost before the submission period may be disqualified.

## Dates and milestones

All official-rules times are Pacific Time:

| Milestone | Formal rules | Stockholm conversion |
| --- | --- | --- |
| Registration | Jul 9, 10:00–Jul 21, 17:00 | Jul 9, 19:00–Jul 22, 02:00 CEST |
| Submission | Jul 13, 09:00–Jul 21, 17:00 | Jul 13, 18:00–Jul 22, 02:00 CEST |
| Judging | Jul 22, 10:00–Aug 5, 17:00 | Jul 22, 19:00–Aug 6, 02:00 CEST |
| Winners announced | On or around Aug 12, 14:00 | On or around Aug 12, 23:00 CEST |

The Devpost key-dates API, retrieved at the same time, reports submission end as `2026-07-22T00:00:00Z` (consistent with July 21, 17:00 PT) and winners as `2026-08-12T21:00:00Z`. It reports a judging end that differs from the formal rules; treat the [official rules](https://openai.devpost.com/rules) as authoritative and re-check for updates.

**Optional credits:** the rules say registered entrants may request $100 in free credits (while supplies last, subject to approval) via the referenced form by **July 17, 12:00 PT**; credits must be used by July 31. Any use beyond provided credits is the entrant’s responsibility.

## Tracks and prizes

Choose the best-fit category:

- **Apps for Your Life:** consumer products for everyday life.
- **Work & Productivity:** tools for teams, workflows, support, analytics, sales, or operations.
- **Developer Tools:** developer-facing testing, DevOps, agentic-workflow, or security tools.
- **Education:** AI projects for students, teachers, or educational organizations.

The total listed prize pool is **$100,000 USD**. Each track has one $15,000 first prize and one $10,000 second prize. First-place packages also list up to two DevDay/Exchange passes (travel not included), OpenAI developer promotion, a Codex-team meeting, and one year of Pro; second place lists promotion and one year of Pro. Each project is eligible for one prize only.

## What the judges evaluate

The formal rules describe a Stage One viability pass/fail (fits the theme and reasonably applies the required tools), then Stage Two. These criteria are **equally weighted**:

1. **Technological Implementation** — skillful Codex use; genuine effort; working, non-trivial implementation.
2. **Design** — a working/runnable project with a complete, coherent product experience, not merely a technical proof of concept.
3. **Potential Impact** — a credible, specific real problem and audience, with evidence that the solution addresses it.
4. **Quality of the Idea** — creativity/novelty and understanding of the problem space.

Tie-breaking follows the listed criterion order, beginning with Technological Implementation.

## Submission package and planner checklist

### Scope guardrails

- [ ] Select one track and state the user, problem, and outcome in one sentence.
- [ ] Define a narrow, demoable end-to-end workflow that will be runnable by the deadline.
- [ ] Use Codex and GPT-5.6 in a way the team can truthfully explain and evidence.
- [ ] If reusing code, document exactly what predates July 13 and what meaningful extension was made during the period; retain dated commits/session evidence.
- [ ] Confirm licences, API/data permissions, ownership, and lack of third-party-IP infringement.
- [ ] Prefer no-login/free judge access; otherwise prepare reliable credentials and instructions.

### Required submission materials

- [ ] Working project and selected category.
- [ ] Clear project description explaining features and functionality.
- [ ] **Public YouTube video <3 minutes**: show the project working; use audio/voiceover covering what was built and how Codex and GPT-5.6 were used. Do not use unlicensed music/trademarks/material.
- [ ] Repository URL: public with relevant licence, or private with access shared to `testing@devpost.com` and `build-week-event@openai.com`.
- [ ] README: setup, sample data when needed, running/testing guidance, and a concrete account of how Codex accelerated work, key product/engineering/design decisions, and GPT-5.6/Codex contribution.
- [ ] `/feedback` Codex Session ID for the thread where the majority of core functionality was built.
- [ ] Test URL/demo/test build and any credentials, kept available free of charge through the judging period.
- [ ] For plugins/developer tools: installation instructions, supported platforms, and a judge testing path (demo instance, sandbox, or test account).
- [ ] Check all team members are added and invitations accepted; submit rather than leaving a draft.

## Sources

- [OpenAI Build Week event page](https://openai.devpost.com/) — overview, tracks, resources, and current event status.
- [Official Rules](https://openai.devpost.com/rules) — eligibility, dates, requirements, IP, judging, prizes, and legal terms.
- Devpost Hackathons connected-service reads on 2026-07-13 17:33 UTC: `get_hackathon_overview`, `get_hackathon_rules`, `get_key_dates`, `get_judging_criteria`, `get_prizes`, `get_submission_requirements`, and `get_announcements`.

The official rules explicitly say the Devpost plugin is a convenience and that the rules, event website, and sponsor/administrator notices prevail. Re-check those sources immediately before submission.
