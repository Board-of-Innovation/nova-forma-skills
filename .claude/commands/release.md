---
description: Prepare a release locally (version, CHANGELOG, checks, zips), then stop and hand the maintainer the tag and push commands
argument-hint: "[patch | minor | major | X.Y.Z]"
disable-model-invocation: true
---

Prepare release `$ARGUMENTS` of the Nova Forma skills. You prepare everything on this machine; the maintainer tags and pushes. Never run `git tag`, `git push`, `gh release` or any other command that publishes, and never commit unless the maintainer asks.

1. **Pick the version.** Read the current `version` in `.claude-plugin/plugin.json`. Work out the new one from `$ARGUMENTS`: `patch`, `minor`, `major` or an exact `X.Y.Z`. When `$ARGUMENTS` is empty, read `## [Unreleased]` in `CHANGELOG.md` and propose one (patch for fixes and wording, minor for new behaviour, major for changes users must adapt to), then wait for the maintainer to confirm.
2. **Check the starting point.** Run `git status`. Stop and ask when there are uncommitted changes that are not part of this release. When on `main`, create a local branch `release/vX.Y.Z` first.
3. **Bump the version everywhere.** Set `version` in `.claude-plugin/plugin.json`, and `metadata.version` (in double quotes) in every `skills/*/SKILL.md`. Nothing else holds the version: `marketplace.json` must not.
4. **Update the CHANGELOG.** Move everything under `## [Unreleased]` into a new section `## [X.Y.Z] - YYYY-MM-DD` with today's date, and leave an empty `## [Unreleased]` above it. Update the links at the bottom: `[Unreleased]` compares `vX.Y.Z...HEAD`, and `[X.Y.Z]` compares the previous tag with `vX.Y.Z` (for the first release, link to `releases/tag/vX.Y.Z`). When `## [Unreleased]` is empty, stop and ask what the release contains.
5. **Run every check** the way `/check` does, and fix what fails. A release never goes out with a failing check.
6. **Build the zips** with `python3 scripts/build_zips.py` and list them with their sizes. When skill content changed since the last release, remind the maintainer to test-upload one zip from `dist/` in Claude (Customize > Skills, then **+**, **Create skill** and **Upload a skill**) before tagging.
7. **Show the result**: the files you changed and the new CHANGELOG section.
8. **Stop here.** Give the maintainer these commands with the real version filled in, and explain each line in a few words:

   ```sh
   git add .claude-plugin/plugin.json skills/*/SKILL.md CHANGELOG.md
   git commit -m "Release vX.Y.Z"
   git push -u origin release/vX.Y.Z
   # open a pull request, wait for the Validate workflow to pass, then merge it
   git checkout main && git pull
   git tag -a vX.Y.Z -m "Nova Forma skills vX.Y.Z"
   git push origin vX.Y.Z
   ```

   Then explain what happens next: the Release workflow checks that the tag matches `plugin.json`, runs the checks, builds the four zips, creates a draft release with the notes from the CHANGELOG section, attaches the zips and publishes it. The maintainer can follow it under the repository's Actions tab and see the result on its Releases page. A published release cannot be changed: to correct one, release a new patch version.
