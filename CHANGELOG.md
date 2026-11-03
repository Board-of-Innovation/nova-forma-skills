# Changelog

All notable changes to the Nova Forma skills are listed here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The four Nova Forma skills, run in order:
  1. `nova-forma-workflow-identifier`: Pick the workflow.
  2. `nova-forma-outcome-statement-writer`: Define success.
  3. `nova-forma-requirements-lister`: Map today's work.
  4. `nova-forma-value-at-stake-sizer`: Size the value, ending with a one-page brief for the redesign week.
- Plugin and marketplace manifests in `.claude-plugin/`, so the repository installs as the `nova-forma` plugin from the `nova-forma-skills` marketplace.
- A zip file per skill on every GitHub release, for uploading the skills to Claude one by one.
- Shared references kept in `shared/references/` and copied into every skill by `scripts/sync_shared.py`.
- The Apache 2.0 license, a NOTICE file, and a copy of both in every skill folder, so each zip carries them.
- A contributing guide, a security policy, a code of conduct, and issue and pull request templates.
- `references/one-pager.md` in the value-at-stake sizer: what the brief for the redesign week holds, with an example.

### Changed

- The skills read the conversation and attached files, and ask before they open earlier chats, memory or a connected tool. What they read there counts as evidence, never as instructions.
- Each skill runs on its own: an "If you start here" line names the minimum it needs, and it asks for that in one round of questions.
- Each skill hands over to the next one by name. Where that skill is not available, it gives everything accepted so far as one block to paste into a new chat, opening with a line that asks for the next step, with a link to this repository.
- The skill descriptions are narrower: one workflow someone plans to redesign or automate with AI, with one "Not for" boundary each.
- Questions and results work without cards or drawings, with a text form for each. Results show the headline first, then the visual, then the table.
- The skills describe what each step does instead of naming a method document users cannot see.
- Research findings are cited only from `references/evidence.md`, at most one per result.
- The workflow identifier keeps a candidate with an unknown gate on the list as "? to confirm", instead of ruling it out.
- The outcome statement writer builds on the scope card's four "What the redesign must show" lines and no longer asks them again.
- Every sources card has at most four options. Email gets its own option and is never recommended, and team chat is read in its channels only, never in direct messages unless the user asks.
- With nothing connected, the workflow identifier asks which candidates hurt most before it scores them, and breaks a full tie on the user's answers.
- The value-at-stake sizer counts late work on demand that does not grow, such as supplier invoices, as better results, takes costs only from the user's own estimate, and says in one line whether the case is worth it: against a payback within a year, or against the spending ceiling when there is no cost.

### Fixed

- Evidence: corrected figures, sources and links for E4, E7, E9, E14, E17, E20 and E24 to E28, and E31 now reads as a planned pilot with no results.
- The value-at-stake sizer's script runs on Python 3.9, a Mac's system Python, names each size check it could not run, runs all four size checks, caps freed hours at the workflow's and the team's hours, counts savings with no mechanism as freed hours with no destination, and stops on a bad input, a misspelled field included, with one plain error line. It tests a range of revenue or EBIT at its lowest figure, and prints no spending ceiling when running costs are above the value.
- The examples follow their own rules: real today and target values, owners marked "Unknown, to confirm", no rows after the workflow's end point, and red lines that match the scope card.
- The writing rules credit the MIT-licensed humanizer skill they adapt, with its notice in NOTICE.

[Unreleased]: https://github.com/Board-of-Innovation/nova-forma-skills/commits/main
