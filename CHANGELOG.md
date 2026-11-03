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
- The Apache 2.0 license, a NOTICE file and a license copy in every skill folder.
- A contributing guide, a security policy, a code of conduct, and issue and pull request templates.

[Unreleased]: https://github.com/Board-of-Innovation/nova-forma-skills/commits/main
