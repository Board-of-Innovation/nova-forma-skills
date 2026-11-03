# Contributing

Thank you for helping improve the Nova Forma skills. Issues and pull requests are welcome.

## First: this repository is public

Anyone can read what you write here: issues, pull requests, comments and commits.

- Never paste confidential company data, client or customer names, personal data or internal links into an issue or pull request.
- Invent your examples. Use made-up companies, round numbers and roles instead of names.
- Before you share a skill's result, remove anything that could identify a company or a person.
- Your commits show the email address in your git settings. To keep yours private, use the no-reply address GitHub gives you, as [Setting your commit email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) explains.

## Ways to help

- Open a skill feedback issue when a result was weak, wrong or confusing.
- Open a bug report for a problem with installing or with the script.
- Open a pull request for a fix or an improvement. For a larger change, open an issue first so we can agree on the approach.
- Report a security problem as [SECURITY.md](SECURITY.md) describes, never in a public issue.

## How the repository works

```
skills/<skill-name>/     one folder per skill
  SKILL.md               what the skill does and how it runs
  references/            detail the skill reads when it needs it
  LICENSE.txt            a copy of the license, so each skill can travel on its own
shared/references/       the four files every skill shares
scripts/                 the check, sync and zip scripts
.claude-plugin/          the plugin and marketplace manifests
AGENTS.md                the guide for AI coding assistants that work on this repository
```

- Edit a skill in its own folder under `skills/`. Skill names are fixed: renaming a folder or its `name` breaks existing installs.
- The four shared files, `context.md`, `display.md`, `evidence.md` and `writing.md`, are the same in every skill. Edit them only in `shared/references/`, then run `python3 scripts/sync_shared.py` to copy them into every skill. Never edit the copies in `skills/*/references/`: the check fails when they drift.
- The block at the top of each `SKILL.md`, its frontmatter, uses only the six fields of the [Agent Skills specification](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. Claude rejects an uploaded skill with any other field.
- Add no symlinks and no zip files. The release zips are built automatically.
- When a change alters what a skill does, add a line under Unreleased in [CHANGELOG.md](CHANGELOG.md). Leave the version as it is: the maintainers change it when they release, as the release steps in [AGENTS.md](AGENTS.md) describe.

Before you open a pull request, run the checks and fix what they report:

```
python3 scripts/check.py
```

The automatic checks on every pull request also run a few more validators. [AGENTS.md](AGENTS.md) lists them, with the commands to run them yourself.

To try your local copy in Claude Code for one session, run `claude --plugin-dir .` from the repository folder.

## Writing style

The skills are written for business owners and managers who are new to AI. Follow [shared/references/writing.md](shared/references/writing.md), copied into every skill as `skills/*/references/writing.md`. It applies to skill text and documentation alike: short sentences, plain words and no dashes as punctuation.

## License of your contribution

This repository is licensed under [Apache 2.0](LICENSE). Under section 5 of that license, anything you submit is licensed under the same terms. There is no separate agreement to sign. Submit only work you wrote or have the right to share, and quote other sources briefly, with where they come from.

## Code of Conduct

Everyone who takes part follows the [Code of Conduct](CODE_OF_CONDUCT.md).
