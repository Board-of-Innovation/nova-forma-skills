---
paths:
  - "skills/**"
  - "shared/**"
---

# Editing the skills

These rules apply whenever you change a file under `skills/` or `shared/`. AGENTS.md has the full reasons.

- **Shared files.** `context.md`, `display.md`, `evidence.md` and `writing.md` are edited only in `shared/references/`. After the edit, run `python3 scripts/sync_shared.py` so all four skills get the same copy. Never edit `skills/*/references/` copies of these four files. If you find an edit in a copy, move it into `shared/references/` first, then sync.
- **Frontmatter.** Only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. The `name` is unquoted and equals the folder name. Keep `license: Apache-2.0` and the `metadata` block with `author: Board of Innovation` and a quoted `version` that equals the version in `.claude-plugin/plugin.json`. Change the version only as part of a release.
- **Names.** Never rename a skill, its folder or its `name`. Write skill names in full and in lowercase, exactly as they are.
- **Self-contained.** Every file a skill mentions must exist in that skill's folder. No `../` paths, no links into another skill, no symlinks. A skill-specific file belongs in that skill's `references/`, never in `shared/references/`.
- **Size.** Keep `SKILL.md` under 500 lines and the `description` under 1,024 characters. Put detail in `references/`.
- **Plain-text fallback.** Every question card, inline form, visual or attachment needs a stated fallback for apps that cannot show it.
- **Evidence and examples.** Figures come from public sources with a working link, quoted as the source states them. Examples are invented and obviously illustrative: round numbers, roles instead of names, no real company or client.
- **Scripts.** Standard library only, no network calls, called by a path relative to `SKILL.md`. Python files carry `# SPDX-License-Identifier: Apache-2.0`.
- **Writing.** Plain English for business readers who are new to AI, following `references/writing.md`. No em or en dashes.
- **Afterwards.** Run `python3 scripts/check.py`, and add a line under `## [Unreleased]` in `CHANGELOG.md` when the change alters what a skill does.
