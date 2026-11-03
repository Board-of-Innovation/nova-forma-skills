# AGENTS.md

How to work on the Nova Forma skills. This guide is for anyone who changes this repository, people and AI coding agents alike. Claude Code reads it through `.claude/CLAUDE.md`.

## Public-repo rules: read these first

This repository is public. Anyone can read every file, commit message, branch name, pull request, issue and comment, and git keeps deleted text in its history. So these rules apply everywhere, not only to files:

- **Never add client details.** No client or prospect names, no project code names, and no detail that points to one company, such as a sector plus a size plus a city.
- **Never add Board of Innovation internals.** No internal team, project or tool names, and no internal documents or excerpts from them.
- **Never add links to internal tools or documents.** That covers Slack, Notion, Google Drive and Docs, Linear, Granola, Jira and Confluence, Miro, Figma and private GitHub repositories. The only Board of Innovation links allowed are <https://novaforma.ai> and <https://www.boardofinnovation.com>.
- **Never add personal data.** No email addresses, phone numbers or names of people who are not public authors.
- **Never add unpublished figures.** No prices, rates, margins, pipeline or client results that Board of Innovation has not published.
- **Never add secrets.** No keys, tokens or passwords.
- **Evidence comes only from public sources, with a link to each one.** Quote a figure the way the source states it, with its year. If you cannot link to a source, leave the figure out.
- **Examples are invented and obviously illustrative.** Use round numbers, made-up company types and roles instead of names. Never adapt a real client case into an example.
- **Private terms stay in `.denylist.local`.** Maintainers keep the client and project names to block in a `.denylist.local` file at the repository root, one term per line (lines starting with `#` are comments). The file is gitignored. Never commit it, and never copy its terms into any other file. `python3 scripts/check.py` reads it and fails on every match.
- **If something private lands by mistake,** a new commit that deletes it is not enough, because the history keeps it. Stop and tell a maintainer, who removes it from the history before anything is pushed, or treats it as leaked if it was pushed.

Internal discussion about clients, pricing or plans belongs in Board of Innovation's own tools, never in issues or pull requests here.

## What is where

```text
.claude-plugin/
  marketplace.json      the marketplace "nova-forma-skills", with one plugin, source "./"
  plugin.json           the plugin "nova-forma": version, description, license, icon
  icon.png              the plugin's icon for Anthropic's plugin directory
skills/<skill-name>/    one folder per skill, each one complete on its own
  SKILL.md              frontmatter plus the instructions Claude follows
  LICENSE.txt           a copy of the root LICENSE
  references/           detail the skill reads when it needs it
  scripts/              code the skill runs (only the value-at-stake sizer has one)
shared/references/      the one place to edit context.md, display.md, evidence.md, writing.md
scripts/
  check.py              every repository check in one command
  sync_shared.py        copies shared/references/ and LICENSE into every skill
  build_zips.py         builds dist/<skill-name>.zip for uploading one skill to Claude
.github/                CI workflows, issue and pull request templates, CODEOWNERS, Dependabot
.claude/                Claude Code settings, path rules and maintainer commands
```

The repository is both the marketplace and the plugin, so users install it as `nova-forma@nova-forma-skills`. Two things must never exist: a top-level `bin/` folder (claude.ai refuses a plugin with one) and a `CLAUDE.md` at the root (it makes `claude plugin validate --strict` fail; Claude Code's file lives in `.claude/CLAUDE.md`).

## How the four skills chain

The skills form the intake for a Nova Forma redesign and run in this order:

1. `nova-forma-workflow-identifier`, **Pick the workflow**: a ranked shortlist, the user's pick and a scope card.
2. `nova-forma-outcome-statement-writer`, **Define success**: one outcome statement, its measures, principles and red lines.
3. `nova-forma-requirements-lister`, **Map today's work**: every requirement and exception, with owners and steps.
4. `nova-forma-value-at-stake-sizer`, **Size the value**: a yearly value range, then a one-page brief for the redesign week.

Each skill reads what the earlier steps produced in the conversation and ends by offering the next step. Each one must still work on its own: when an earlier result is missing, it asks for the core of it first. Users need a paid Claude plan with code execution switched on (whether the Free plan works is still to be tested).

## Editing rules

- **Shared files.** `context.md`, `display.md`, `evidence.md` and `writing.md` are identical in all four skills. Edit them only in `shared/references/`, run `python3 scripts/sync_shared.py`, and commit the shared file together with its four copies. Never edit a copy under `skills/*/references/`: the check fails, and the next sync overwrites it. No symlinks, anywhere.
- **Names are frozen.** The plugin `nova-forma`, the marketplace `nova-forma-skills` and the four skill names stay as they are: renaming one breaks every install. Write a skill's name exactly as it is, in full and in lowercase, such as `nova-forma-requirements-lister`, never a shortened or differently written form.
- **Frontmatter uses only the six Agent Skills keys**: `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. claude.ai rejects an upload with any other key. The `name` is unquoted and equals the folder name. The `description` says what the skill does and when to use it, in at most 1,024 characters, with no XML tags. Every skill has this shape:

  ```yaml
  ---
  name: nova-forma-workflow-identifier
  description: What the skill does, and when to use it.
  license: Apache-2.0
  metadata:
    author: Board of Innovation
    version: "1.0.0"
  ---
  ```

- **Keep each skill self-contained.** Every file a skill mentions lives in its own folder, because a zip upload holds one skill folder and nothing else. No `../` paths and no links into another skill. Keep `SKILL.md` under 500 lines and move detail into `references/`.
- **Give every host-specific feature a plain-text fallback.** Question cards, inline forms, drawn visuals and file attachments exist only in some apps. Wherever a skill uses one, it also says what to do without it, such as "Without cards, end with: Reply Accept to go to step 2."
- **Scripts in skills** use only the Python standard library, make no network calls, and are called by a path relative to `SKILL.md`, such as `scripts/value_case.py`.
- **Python files** start with `# SPDX-License-Identifier: Apache-2.0`, on the second line when the first is a `#!` line.
- **Write plain English** for business owners and managers who are new to AI, following `shared/references/writing.md`. Use no em or en dashes: use a comma, a colon or a full stop.
- **Maintainer helpers for Claude Code** go in `.claude/commands/`, never in `.claude/skills/`, because `npx skills` would offer those to end users.

## Checks

Run this before every commit. It needs only Python 3.10 or later:

```sh
python3 scripts/check.py
```

It checks the frontmatter of every skill against the Agent Skills specification, that every file a skill mentions exists in that skill, that the shared files and LICENSE copies are in sync, that the manifests parse and agree, that no symlinks, junk files or zips are in the tree, that Python files carry the license header, which files `ruff.toml` keeps out of the Python lint, and the public-repo denylist: email addresses, links to internal tools, wording that marks material as private, keys and tokens, and the terms in your `.denylist.local`. Each failure says how to fix it.

CI runs the same command in `.github/workflows/validate.yml` on every pull request and every push to `main`, together with these validators. Run them locally with the versions pinned in that file:

```sh
for d in skills/*/; do uvx --from skills-ref==0.1.1 agentskills validate "$d"; done
uvx ruff@0.17.1 check . && uvx ruff@0.17.1 format --check .
npx --yes markdownlint-cli2@0.24.0
npx --yes @anthropic-ai/claude-code@2.1.311 plugin validate . --strict
python3 scripts/build_zips.py
```

Never weaken a check or a lint rule to make a failure go away. In Claude Code, `/check` runs everything and explains each failure, and `/public-review` reviews a change against the rules above.

## Versioning

The library has one version, a semantic version such as `1.0.0`. It lives in `.claude-plugin/plugin.json` and is copied into `metadata.version` in every `SKILL.md`; `check.py` fails when they differ. The marketplace entry holds no version.

The version changes only as part of a release. A pull request that changes a skill adds a line under `## [Unreleased]` in `CHANGELOG.md` and leaves the version alone. Bump the version on every release, because Claude Code only offers users an update when the version changes:

- **Patch** (1.0.1): fixes and clearer wording.
- **Minor** (1.1.0): new behaviour, a new question or a new reference.
- **Major** (2.0.0): a change users must adapt to, such as a different chain or a different result.

## Releasing

1. Bump the version in `.claude-plugin/plugin.json` and in `metadata.version` of all four `SKILL.md` files.
2. In `CHANGELOG.md`, move the items under `## [Unreleased]` into a new `## [X.Y.Z] - YYYY-MM-DD` section and update the links at the bottom.
3. Run `python3 scripts/check.py` and the validators above, then `python3 scripts/build_zips.py`. When skill content changed, test-upload one zip from `dist/` in Claude before you tag.
4. Open a pull request, wait for the Validate workflow to pass, and merge it into `main`.
5. Tag the merge commit and push the tag:

   ```sh
   git checkout main && git pull
   git tag -a vX.Y.Z -m "Nova Forma skills vX.Y.Z"
   git push origin vX.Y.Z
   ```

6. The Release workflow (`.github/workflows/release.yml`) checks that the tag matches `plugin.json`, runs the checks, builds the four zips, creates a draft release with the notes from the CHANGELOG section, attaches the zips and then publishes the release. The asset names never change, so links such as <https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest/download/nova-forma-workflow-identifier.zip> always serve the newest version.

Published releases are immutable. To correct one, release a new patch version. AI agents never tag, push or publish: in Claude Code, `/release` prepares steps 1 to 3 and then hands the maintainer the exact commands.
