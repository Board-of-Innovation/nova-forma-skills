---
description: Run every repository check and CI validator, explain each failure and fix what is safe to fix
---

Run all the checks for this repository, explain every failure in plain words, and fix what can be fixed safely.

1. Run `python3 scripts/check.py`.
2. Run the validators that CI runs. Read the `env` block in `.github/workflows/validate.yml` first and use exactly the versions pinned there:
   - `for d in skills/*/; do uvx --from skills-ref==<SKILLS_REF_VERSION> agentskills validate "$d"; done`
   - `uvx ruff@<RUFF_VERSION> check .` and `uvx ruff@<RUFF_VERSION> format --check .`
   - `npx --yes markdownlint-cli2@<MARKDOWNLINT_CLI2_VERSION>`
   - `HOME="$(mktemp -d)" npx --yes @anthropic-ai/claude-code@<CLAUDE_CODE_VERSION> plugin validate . --strict`
   - `python3 scripts/build_zips.py`

   When a tool is missing (uv or Node.js), say which one and skip that validator rather than installing anything globally.
3. For each failure, explain what failed, why it matters to someone installing the skills, and the fix.
4. Fix what is safe to fix:
   - Shared files out of sync: if a copy inside a skill holds an edit, move that edit into `shared/references/` first, then run `python3 scripts/sync_shared.py`. Never throw away someone's edit.
   - Formatting: `uvx ruff@<RUFF_VERSION> format .`, then check again.
   - Frontmatter, manifests and paths: fix them as the error message says.
5. Do not fix these yourself, report them to the maintainer instead:
   - Any public-repo denylist finding. It may be private material: name the file and line, quote at most a few words, and suggest a rewrite.
   - Anything that would weaken a check, change a lint rule, add an entry to `REVIEWED_ALLOW` in `scripts/check.py`, or change `.denylist.local`.
   - Content changes to a skill that go beyond the fix the error asks for.
6. Run everything again until it passes, then end with a short table: check, result, and what you changed.

Never commit, push, tag or publish anything.
