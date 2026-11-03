#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Copy the shared files into every skill, or check that the copies match.

Every skill must work on its own (a zip upload holds one skill folder), so the
files that all four skills share live in shared/references/ and are copied,
never symlinked, into skills/<name>/references/. The root LICENSE is copied to
skills/<name>/LICENSE.txt the same way.

Usage:
    python3 scripts/sync_shared.py          # write the copies
    python3 scripts/sync_shared.py --check  # report drift, exit 1 if any
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = Path("shared/references")
LICENSE = Path("LICENSE")
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


@dataclass(frozen=True)
class Copy:
    """One file that must be a byte-identical copy of another."""

    source: Path
    target: Path
    kind: str  # "shared" or "license"


@dataclass(frozen=True)
class Drift:
    copy: Copy
    reason: str


def skill_dirs(root: Path = ROOT) -> list[Path]:
    """Every folder under skills/ that holds a SKILL.md, sorted by name."""
    skills = root / "skills"
    if not skills.is_dir():
        return []
    return sorted(p for p in skills.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def shared_files(root: Path = ROOT) -> list[Path]:
    """The canonical shared files, relative to the repo root."""
    folder = root / SHARED_DIR
    if not folder.is_dir():
        return []
    return sorted(
        (SHARED_DIR / p.name)
        for p in folder.iterdir()
        if p.is_file() and not p.is_symlink() and p.name not in JUNK_NAMES
    )


def planned_copies(root: Path = ROOT) -> list[Copy]:
    copies: list[Copy] = []
    sources = shared_files(root)
    has_license = (root / LICENSE).is_file()
    for skill in skill_dirs(root):
        rel = skill.relative_to(root)
        for src in sources:
            copies.append(Copy(src, rel / "references" / src.name, "shared"))
        if has_license:
            copies.append(Copy(LICENSE, rel / "LICENSE.txt", "license"))
    return copies


def find_drift(root: Path = ROOT, kinds: tuple[str, ...] = ("shared", "license")) -> list[Drift]:
    """Return every copy that is missing, a symlink, or different from its source."""
    drift: list[Drift] = []
    for copy in planned_copies(root):
        if copy.kind not in kinds:
            continue
        target = root / copy.target
        if target.is_symlink():
            drift.append(Drift(copy, "is a symlink; it must be a real copy"))
        elif not target.is_file():
            drift.append(Drift(copy, "is missing"))
        elif target.read_bytes() != (root / copy.source).read_bytes():
            drift.append(Drift(copy, f"differs from {copy.source}"))
    return drift


def sync(root: Path = ROOT) -> list[Drift]:
    """Write every copy that drifted. Returns what was written and why."""
    written: list[Drift] = []
    for item in find_drift(root):
        target = root / item.copy.target
        if target.is_symlink():
            target.unlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((root / item.copy.source).read_bytes())
        written.append(item)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="report drift and exit 1 instead of writing"
    )
    args = parser.parse_args(argv)

    if not shared_files():
        print(f"No shared files found in {SHARED_DIR}/.", file=sys.stderr)
        return 1
    if not skill_dirs():
        print("No skills found under skills/.", file=sys.stderr)
        return 1

    if args.check:
        drift = find_drift()
        if not drift:
            print("Shared files and LICENSE copies are in sync.")
            return 0
        print("These copies are out of sync:")
        for item in drift:
            print(f"  {item.copy.target} {item.reason}")
        print(
            "Fix: edit the file in shared/references/ (or the root LICENSE), "
            "then run: python3 scripts/sync_shared.py"
        )
        return 1

    written = sync()
    if not written:
        print("Nothing to do: every copy already matches.")
    for item in written:
        print(f"wrote {item.copy.target} (it {item.reason})")
    if any(item.reason.startswith("differs") for item in written):
        print(
            "Note: a copy inside a skill was different and has been replaced. "
            "Edits to shared files belong in shared/references/ (or the root LICENSE)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
