#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build one zip per skill for uploading to Claude, then verify each zip.

Each zip is dist/<skill-name>.zip and holds the skill folder itself at the top
level (<skill-name>/SKILL.md), which is what a claude.ai skill upload expects.
The build is deterministic: entries are sorted, timestamps and permissions are
fixed, and junk files are left out, so the same commit always gives the same
bytes.

Usage:
    python3 scripts/build_zips.py              # writes dist/<skill-name>.zip
    python3 scripts/build_zips.py --out build  # writes build/<skill-name>.zip
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
FIXED_TIME = (1980, 1, 1, 0, 0, 0)  # the earliest timestamp a zip can hold
JUNK_NAMES = {".DS_Store", "__MACOSX", "__pycache__", "Thumbs.db", "desktop.ini"}
JUNK_SUFFIXES = (".pyc", ".pyo")


def is_junk(name: str) -> bool:
    return name in JUNK_NAMES or name.startswith("._") or name.endswith(JUNK_SUFFIXES)


def collect(skill: Path) -> tuple[list[PurePosixPath], list[PurePosixPath]]:
    """Return the sorted folders and files to pack, relative to skills/."""
    base = skill.parent
    folders: list[PurePosixPath] = [PurePosixPath(skill.name)]
    files: list[PurePosixPath] = []
    stack = [skill]
    while stack:
        current = stack.pop()
        for entry in current.iterdir():
            if is_junk(entry.name):
                continue
            rel = PurePosixPath(entry.relative_to(base).as_posix())
            if entry.is_symlink():
                raise SystemExit(
                    f"error: {entry.relative_to(ROOT)} is a symlink. "
                    "Replace it with a real file; zips must not contain links."
                )
            if entry.is_dir():
                folders.append(rel)
                stack.append(entry)
            elif entry.is_file():
                files.append(rel)
    return sorted(folders), sorted(files)


def write_zip(skill: Path, out: Path) -> Path:
    folders, files = collect(skill)
    target = out / f"{skill.name}.zip"
    entries: list[tuple[str, Path | None]] = [(f"{d}/", None) for d in folders]
    entries += [(str(f), skill.parent / f) for f in files]
    entries.sort(key=lambda item: item[0])
    tmp = target.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp, "w") as zf:
        for name, source in entries:
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.create_system = 3  # Unix, so permissions read the same everywhere
            if source is None:
                info.external_attr = (0o40755 << 16) | 0x10
                zf.writestr(info, b"")
            else:
                mode = 0o755 if source.stat().st_mode & 0o111 else 0o644
                info.external_attr = (0o100000 | mode) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, source.read_bytes(), compresslevel=9)
    tmp.replace(target)
    return target


def verify(zip_path: Path, skill: Path) -> list[str]:
    """Re-open a zip and return a list of problems (empty when it is good)."""
    name = skill.name
    problems: list[str] = []
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        bad = zf.testzip()
        if bad:
            problems.append(f"entry {bad} is corrupt")
    if f"{name}/SKILL.md" not in names:
        problems.append(f"{name}/SKILL.md is missing at the top level")
    if names != sorted(names):
        problems.append("entries are not sorted")
    for entry in names:
        parts = PurePosixPath(entry).parts
        if entry.startswith("/") or ".." in parts:
            problems.append(f"unsafe path {entry}")
        if not entry.startswith(f"{name}/"):
            problems.append(f"{entry} is outside the {name}/ folder")
        if any(is_junk(part) for part in parts):
            problems.append(f"junk file {entry}")
    _, files = collect(skill)
    expected = {str(f) for f in files}
    packed = {n for n in names if not n.endswith("/")}
    for missing in sorted(expected - packed):
        problems.append(f"{missing} is in the skill but not in the zip")
    for extra in sorted(packed - expected):
        problems.append(f"{extra} is in the zip but not in the skill")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="dist", help="output folder (default: dist)")
    args = parser.parse_args(argv)

    skills_dir = ROOT / "skills"
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if not skills:
        print("error: no skills found under skills/", file=sys.stderr)
        return 1

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)

    failed = False
    for skill in skills:
        zip_path = write_zip(skill, out)
        problems = verify(zip_path, skill)
        digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()[:12]
        size_kb = zip_path.stat().st_size / 1024
        shown = zip_path.relative_to(ROOT) if zip_path.is_relative_to(ROOT) else zip_path
        if problems:
            failed = True
            print(f"FAIL {shown}")
            for problem in problems:
                print(f"     {problem}")
        else:
            print(f"ok   {shown}  {size_kb:.1f} KB  sha256 {digest}")
    if failed:
        print("Some zips failed verification. Fix the problems above and build again.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
