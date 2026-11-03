#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run every repository check and explain how to fix what fails.

Usage:
    python3 scripts/check.py

Exit code 0 means every check passed (warnings are allowed), 1 means at least
one check failed. CI runs this same command, so a green run here means the
repository checks in CI pass too. The other validators (skills-ref, ruff,
markdownlint and claude plugin validate) run in .github/workflows/validate.yml.

Uses only the Python standard library (Python 3.10 or later).
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of the repo, the junk check looks for it

import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from pathlib import Path  # noqa: E402

import sync_shared  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# --- What the checks expect --------------------------------------------------

SPEC_KEYS = ("name", "description", "license", "compatibility", "metadata", "allowed-tools")
LICENSE_ID = "Apache-2.0"
AUTHOR = "Board of Innovation"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
RESERVED_WORDS = ("anthropic", "claude")
MAX_NAME, MAX_DESCRIPTION, MAX_COMPATIBILITY, MAX_SKILL_LINES = 64, 1024, 500, 500

PLUGIN_JSON = Path(".claude-plugin/plugin.json")
MARKETPLACE_JSON = Path(".claude-plugin/marketplace.json")

# Folders that are never part of the repository's content.
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".ruff_cache", ".mypy_cache", ".pytest_cache"}
JUNK_NAMES = {".DS_Store", "__MACOSX", "__pycache__", "Thumbs.db"}
JUNK_SUFFIXES = (".pyc", ".pyo", ".zip")
TEXT_SUFFIXES_IN_SKILLS = {".md", ".py", ".json", ".txt", ".csv", ".yaml", ".yml"}

# --- Public-repo denylist ----------------------------------------------------
# This file holds the patterns, so the denylist scan skips it. Client names and
# other private terms never go here: keep them in the gitignored .denylist.local.

DENYLIST_SELF = Path("scripts/check.py")
LOCAL_DENYLIST = Path(".denylist.local")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
ALLOWED_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "users.noreply.github.com")
ALLOWED_EMAILS = ("git@github.com",)
NOT_EMAIL_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")

INTERNAL_HOSTS = (
    r"slack\.com",
    r"notion\.so",
    r"notion\.site",
    r"docs\.google\.com",
    r"drive\.google\.com",
    r"linear\.app",
    r"granola\.ai",
    r"atlassian\.net",
    r"miro\.com",
    r"figma\.com",
)
INTERNAL_HOST_RE = re.compile(
    r"(?<![A-Za-z0-9.-])(?:[A-Za-z0-9-]+\.)*(?:" + "|".join(INTERNAL_HOSTS) + r")(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
BOI_HOST_RE = re.compile(
    r"(?<![A-Za-z0-9.@-])(?:[A-Za-z0-9-]+\.)*boardofinnovation\.[A-Za-z]{2,}(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
ALLOWED_BOI_HOSTS = ("novaforma.ai", "www.boardofinnovation.com")
GITHUB_ORG_RE = re.compile(
    r"github\.com/(Board-of-Innovation[A-Za-z0-9-]*)(?:/([A-Za-z0-9._-]+))?", re.IGNORECASE
)
PUBLIC_ORG, PUBLIC_REPO = "Board-of-Innovation", "nova-forma-skills"

# Markings that label a document as private. Checked in every file.
PRIVATE_MARKING_RE = re.compile(
    r"\b(?:internal[ -]only|internal use only|do not distribute|do not forward"
    r"|not for (?:external )?distribution|confidential and proprietary"
    r"|(?:strictly|company|highly|commercially|privileged and) confidential)\b",
    re.IGNORECASE,
)
CAPS_CONFIDENTIAL_RE = re.compile(r"\bCONFIDENTIAL\b")
# The plain word "confidential" is checked everywhere except in the files whose
# job is to tell readers what not to share (they say "never paste confidential
# data"). Markings above are still checked there.
CONFIDENTIAL_RE = re.compile(r"\bconfidential\b", re.IGNORECASE)
RULE_FILES = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/",
    ".claude/",
)
# Lines a maintainer has reviewed and cleared: (path, exact text on the line).
# Add an entry only after checking the line is fine to publish.
REVIEWED_ALLOW = (
    (
        "skills/nova-forma-outcome-statement-writer/references/examples.md",
        "No other client's confidential data in any draft",
    ),
)

SECRET_PATTERNS = (
    ("a private key", re.compile(r"-----BEGIN[A-Z ]*PRIVATE KEY")),
    (
        "a GitHub token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})"),
    ),
    ("an Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("a Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("an AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
)


# --- Reporting ---------------------------------------------------------------


@dataclass
class Section:
    title: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    skipped: str | None = None

    def error(self, message: str, fix: str | None = None) -> None:
        self.errors.append(message)
        self.add_fix(fix)

    def warn(self, message: str, fix: str | None = None) -> None:
        self.warnings.append(message)
        self.add_fix(fix)

    def add_fix(self, fix: str | None) -> None:
        if fix and fix not in self.fixes:
            self.fixes.append(fix)

    def show(self) -> None:
        if self.skipped:
            status = "SKIP"
        elif self.errors:
            status = "FAIL"
        elif self.warnings:
            status = "WARN"
        else:
            status = "PASS"
        print(f"[{status}] {self.title}")
        if self.skipped:
            print(f"       {self.skipped}")
        for message in self.errors:
            print(f"       error: {message}")
        for message in self.warnings:
            print(f"       warning: {message}")
        for fix in self.fixes:
            print(f"       fix: {fix}")
        for note in self.notes:
            print(f"       note: {note}")
        if os.environ.get("GITHUB_ACTIONS") == "true":
            # Annotations, so warnings show on the run's summary page in GitHub.
            title = escape_annotation(self.title, prop=True)
            for message in self.warnings:
                print(f"::warning title={title}::{escape_annotation(message)}")
            for message in self.errors:
                print(f"::error title={title}::{escape_annotation(message)}")


def escape_annotation(text: str, prop: bool = False) -> str:
    """Escape text for a GitHub Actions workflow command."""
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    if prop:
        text = text.replace(":", "%3A").replace(",", "%2C")
    return text


# --- Files -------------------------------------------------------------------


def run_git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout


def walk(root: Path) -> list[Path]:
    """Every path under root, without following symlinks or entering SKIP_DIRS."""
    found: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        for entry in current.iterdir():
            if entry.name in SKIP_DIRS and entry.is_dir() and not entry.is_symlink():
                continue
            found.append(entry)
            if entry.is_dir() and not entry.is_symlink():
                stack.append(entry)
    return found


def repo_files() -> tuple[list[Path], set[Path], bool]:
    """Files that are or will be committed: tracked plus untracked, not ignored.

    Returns (files relative to ROOT, the tracked subset, whether git was used).
    """
    out = run_git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    tracked_out = run_git("ls-files", "-z", "--cached")
    if out is None or tracked_out is None:
        files = [
            p.relative_to(ROOT)
            for p in walk(ROOT)
            if p.is_file() and not p.is_symlink() and "dist" not in p.relative_to(ROOT).parts[:1]
        ]
        files = [p for p in files if p != LOCAL_DENYLIST]
        return sorted(files), set(), False
    paths = {Path(p) for p in out.split("\0") if p}
    tracked = {Path(p) for p in tracked_out.split("\0") if p}
    existing = sorted(p for p in paths if (ROOT / p).is_file() or (ROOT / p).is_symlink())
    return existing, tracked, True


def read_text(path: Path) -> str | None:
    """Return the file's text, or None for binary or non-UTF-8 files."""
    data = (ROOT / path).read_bytes()
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


# --- A small frontmatter parser ----------------------------------------------
# Skills use a tiny subset of YAML: top-level `key: value` pairs, quoted or
# plain scalars, folded or literal block scalars, and one level of nested
# `key: value` pairs (metadata). Anything else is reported, because a stricter
# YAML parser on claude.ai or in skills-ref may read it differently.


@dataclass
class Scalar:
    value: str
    style: str  # plain, single, double or block
    line: int


class FrontmatterError(Exception):
    pass


KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]+(.*?))?[ \t]*$")
NESTED_RE = re.compile(r"^([ ]+)([A-Za-z0-9_-]+):(?:[ \t]+(.*?))?[ \t]*$")
NON_STRING_RE = re.compile(
    r"^(?:true|false|yes|no|on|off|null|~|[-+]?\d+|[-+]?(?:\d+\.\d*|\.\d+)(?:[eE][-+]?\d+)?"
    r"|\d{4}-\d\d-\d\d)$",
    re.IGNORECASE,
)


def split_frontmatter(text: str) -> tuple[list[str], int]:
    """Return the frontmatter lines and the line number where the body starts."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        raise FrontmatterError("SKILL.md must start with a line that is exactly ---")
    for index in range(1, len(lines)):
        if lines[index].rstrip("\r") == "---":
            return lines[1:index], index + 1
    raise FrontmatterError("the frontmatter has no closing --- line")


def parse_scalar(raw: str, line: int) -> Scalar:
    if not raw:
        return Scalar("", "plain", line)
    if raw.startswith('"'):
        if len(raw) < 2 or not raw.endswith('"'):
            raise FrontmatterError(f"line {line}: a double-quoted value must end on the same line")
        try:
            return Scalar(json.loads(raw), "double", line)
        except json.JSONDecodeError as exc:
            raise FrontmatterError(
                f"line {line}: cannot read the quoted value ({exc.msg})"
            ) from exc
    if raw.startswith("'"):
        if len(raw) < 2 or not raw.endswith("'"):
            raise FrontmatterError(f"line {line}: a single-quoted value must end on the same line")
        return Scalar(raw[1:-1].replace("''", "'"), "single", line)
    if raw[:1] in "[]{}!&*%@`,":
        raise FrontmatterError(
            f"line {line}: a value that starts with {raw[0]!r} has a special meaning in YAML; "
            "put the value in double quotes"
        )
    if raw.startswith("- ") or raw == "-":
        raise FrontmatterError(f"line {line}: lists are not supported here; use a plain string")
    if ": " in raw or raw.endswith(":"):
        raise FrontmatterError(
            f"line {line}: the value contains ': ', which YAML reads as a new key; "
            "put the value in double quotes"
        )
    if " #" in raw or "\t#" in raw:
        raise FrontmatterError(
            f"line {line}: YAML reads ' #' as the start of a comment, so the value would be cut; "
            "put the value in double quotes"
        )
    return Scalar(raw, "plain", line)


def parse_block(indicator: str, lines: list[str]) -> str:
    """Join a | or > block scalar the way YAML does (clip chomping by default)."""
    indents = [len(x) - len(x.lstrip(" ")) for x in lines if x.strip()]
    cut = min(indents) if indents else 0
    body = [x[cut:] if x.strip() else "" for x in lines]
    if indicator.startswith("|"):
        text = "\n".join(body)
    else:
        paragraphs, current = [], []
        for item in body:
            if item:
                current.append(item)
            else:
                paragraphs.append(" ".join(current))
                current = []
        paragraphs.append(" ".join(current))
        text = "\n".join(paragraphs)
    text = text.rstrip("\n")
    if "+" in indicator:
        return text + "\n"
    if "-" in indicator:
        return text
    return text + "\n" if text else text


def parse_frontmatter(lines: list[str]) -> dict[str, Scalar | dict[str, Scalar]]:
    data: dict[str, Scalar | dict[str, Scalar]] = {}
    i = 0
    while i < len(lines):
        line_no = i + 2  # the opening --- is line 1
        line = lines[i].rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterError(f"line {line_no}: unexpected indentation")
        match = KEY_RE.match(line)
        if not match:
            raise FrontmatterError(f"line {line_no}: expected 'key: value'")
        key, raw = match.group(1), match.group(2) or ""
        if key in data:
            raise FrontmatterError(f"line {line_no}: the key '{key}' appears twice")
        # Collect the indented lines that belong to this key.
        j = i + 1
        child: list[str] = []
        while j < len(lines):
            nxt = lines[j].rstrip("\r")
            if nxt.strip() and not nxt.startswith((" ", "\t")):
                break
            child.append(nxt)
            j += 1
        while child and not child[-1].strip():
            child.pop()
        if any(c.startswith("\t") for c in child):
            raise FrontmatterError(f"line {line_no}: use spaces, not tabs, to indent")
        if raw[:1] in ("|", ">") and re.fullmatch(r"[|>][+-]?\d?", raw):
            data[key] = Scalar(parse_block(raw, child), "block", line_no)
        elif raw:
            value = parse_scalar(raw, line_no)
            if child:
                if value.style != "plain":
                    raise FrontmatterError(f"line {line_no + 1}: unexpected indented line")
                # A plain value may continue on indented lines; YAML folds them.
                extra = " ".join(c.strip() for c in child if c.strip())
                value = parse_scalar(f"{value.value} {extra}", line_no)
            data[key] = value
        elif not child:
            data[key] = Scalar("", "plain", line_no)
        else:
            mapping: dict[str, Scalar] = {}
            indent = None
            for offset, item in enumerate(child, start=1):
                if not item.strip() or item.lstrip().startswith("#"):
                    continue
                nested = NESTED_RE.match(item)
                if not nested:
                    raise FrontmatterError(
                        f"line {line_no + offset}: only one level of 'key: value' pairs is "
                        "supported under a key (no lists, no deeper nesting)"
                    )
                if indent is None:
                    indent = nested.group(1)
                elif len(nested.group(1)) > len(indent):
                    raise FrontmatterError(
                        f"line {line_no + offset}: only one level of nesting is supported "
                        f"under '{key}'"
                    )
                elif nested.group(1) != indent:
                    raise FrontmatterError(
                        f"line {line_no + offset}: inconsistent indentation under '{key}'"
                    )
                sub_key, sub_raw = nested.group(2), nested.group(3) or ""
                if sub_key in mapping:
                    raise FrontmatterError(
                        f"line {line_no + offset}: '{key}.{sub_key}' appears twice"
                    )
                mapping[sub_key] = parse_scalar(sub_raw, line_no + offset)
            data[key] = mapping
        i = j
    return data


# --- Checks ------------------------------------------------------------------


def load_json(path: Path, section: Section) -> dict | None:
    full = ROOT / path
    if not full.is_file():
        section.error(f"{path} is missing", f"create {path}; AGENTS.md shows what it holds")
        return None
    try:
        data = json.loads(full.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        section.error(f"{path} is not valid JSON: {exc.msg} at line {exc.lineno}, col {exc.colno}")
        return None
    if not isinstance(data, dict):
        section.error(f"{path} must hold a JSON object")
        return None
    return data


def check_manifests() -> tuple[Section, str | None]:
    section = Section("Plugin and marketplace manifests")
    plugin = load_json(PLUGIN_JSON, section)
    market = load_json(MARKETPLACE_JSON, section)
    version = None
    if plugin is not None:
        name = plugin.get("name")
        if not isinstance(name, str) or not NAME_RE.match(name):
            section.error(f"{PLUGIN_JSON}: 'name' must be kebab-case, found {name!r}")
        elif name.startswith(("claude-", "anthropic-")):
            section.error(f"{PLUGIN_JSON}: the name {name!r} is reserved for Anthropic")
        version = plugin.get("version")
        if not isinstance(version, str) or not SEMVER_RE.match(version):
            section.error(
                f"{PLUGIN_JSON}: 'version' must be a semantic version such as 1.0.0, "
                f"found {version!r}"
            )
            version = None
        if plugin.get("license") != LICENSE_ID:
            section.error(f"{PLUGIN_JSON}: 'license' must be {LICENSE_ID!r}")
        author = plugin.get("author")
        if not isinstance(author, dict) or not author.get("name"):
            section.error(f"{PLUGIN_JSON}: 'author' needs a 'name'")
        elif "email" in author:
            section.error(
                f"{PLUGIN_JSON}: remove 'author.email'; no email addresses in this public repo"
            )
        for key in ("homepage", "repository"):
            value = plugin.get(key)
            if value is not None and not (isinstance(value, str) and value.startswith("https://")):
                section.error(f"{PLUGIN_JSON}: '{key}' must be an https:// URL")
        icon = plugin.get("icon")
        if icon is not None:
            icon_path = (ROOT / str(icon)).resolve()
            if not str(icon).startswith("./") or not icon_path.is_relative_to(ROOT):
                section.error(f"{PLUGIN_JSON}: 'icon' must be a ./ path inside the repo")
            elif not icon_path.is_file():
                section.error(f"{PLUGIN_JSON}: the icon file {icon} does not exist")
    if market is not None:
        if not market.get("name"):
            section.error(f"{MARKETPLACE_JSON}: 'name' is missing")
        owner = market.get("owner")
        if not isinstance(owner, dict) or not owner.get("name"):
            section.error(f"{MARKETPLACE_JSON}: 'owner' needs a 'name'")
        elif "email" in owner:
            section.error(
                f"{MARKETPLACE_JSON}: remove 'owner.email'; no email addresses in this public repo"
            )
        entries = market.get("plugins")
        if not isinstance(entries, list) or not entries:
            section.error(f"{MARKETPLACE_JSON}: 'plugins' must list the plugin")
            entries = []
        plugin_name = plugin.get("name") if plugin else None
        matching = [e for e in entries if isinstance(e, dict) and e.get("name") == plugin_name]
        if plugin_name and not matching:
            section.error(
                f"{MARKETPLACE_JSON}: no entry in 'plugins' is named {plugin_name!r}, "
                f"the name in {PLUGIN_JSON}"
            )
        for entry in matching:
            if entry.get("source") != "./":
                section.error(
                    f'{MARKETPLACE_JSON}: the {plugin_name!r} entry must have "source": "./" '
                    "(this repo is both the marketplace and the plugin)"
                )
            for key in ("strict", "skills"):
                if key in entry:
                    section.error(
                        f"{MARKETPLACE_JSON}: remove '{key}' from the {plugin_name!r} entry; "
                        "with a plugin.json present it makes the plugin fail to load"
                    )
            if "version" in entry:
                section.error(
                    f"{MARKETPLACE_JSON}: remove 'version' from the entry; "
                    f"the version lives only in {PLUGIN_JSON}"
                )
            if not entry.get("description"):
                section.warn(f"{MARKETPLACE_JSON}: the {plugin_name!r} entry has no description")
    return section, version


def check_frontmatter(skills: list[Path], version: str | None) -> Section:
    section = Section("Skill frontmatter (Agent Skills spec)")
    if not skills:
        section.error("no skills found under skills/ (each needs a SKILL.md)")
    for skill in skills:
        rel = skill.relative_to(ROOT) / "SKILL.md"
        raw = (skill / "SKILL.md").read_bytes()
        if b"\r\n" in raw:
            section.error(f"{rel}: uses Windows line endings", "save the file with LF line endings")
        text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
        try:
            lines, body_start = split_frontmatter(text)
            data = parse_frontmatter(lines)
        except FrontmatterError as exc:
            section.error(f"{rel}: {exc}")
            continue

        for key in data:
            if key not in SPEC_KEYS:
                section.error(
                    f"{rel}: unexpected key '{key}'. claude.ai uploads reject any key outside "
                    f"the Agent Skills spec: {', '.join(SPEC_KEYS)}",
                    "move the information into the body of SKILL.md, or delete it",
                )

        name = data.get("name")
        if not isinstance(name, Scalar) or not name.value:
            section.error(f"{rel}: 'name' is missing")
        else:
            if name.style != "plain":
                section.error(f"{rel}: write the name without quotes: name: {name.value}")
            if not NAME_RE.match(name.value):
                section.error(
                    f"{rel}: the name {name.value!r} must be lowercase letters, digits and single "
                    "hyphens, with no hyphen at the start or end"
                )
            if len(name.value) > MAX_NAME:
                section.error(f"{rel}: the name is {len(name.value)} characters; the limit is 64")
            if name.value != skill.name:
                section.error(
                    f"{rel}: the name {name.value!r} must equal the folder name {skill.name!r}"
                )
            if any(word in name.value for word in RESERVED_WORDS):
                section.error(f"{rel}: the name may not contain 'anthropic' or 'claude'")

        description = data.get("description")
        if not isinstance(description, Scalar) or not description.value.strip():
            section.error(f"{rel}: 'description' is missing or empty")
        else:
            length = len(description.value)
            if length > MAX_DESCRIPTION:
                section.error(
                    f"{rel}: the description is {length} characters; the limit is 1024",
                    "shorten the description; say what the skill does and when to use it",
                )
            if re.search(r"<[A-Za-z/][^>]*>", description.value):
                section.error(f"{rel}: the description may not contain XML or HTML tags")

        license_value = data.get("license")
        if not isinstance(license_value, Scalar) or license_value.value != LICENSE_ID:
            section.error(f"{rel}: add 'license: {LICENSE_ID}'")

        compatibility = data.get("compatibility")
        if compatibility is not None and (
            not isinstance(compatibility, Scalar)
            or not compatibility.value.strip()
            or len(compatibility.value) > MAX_COMPATIBILITY
        ):
            section.error(f"{rel}: 'compatibility' must be a string of 1 to 500 characters")

        allowed_tools = data.get("allowed-tools")
        if allowed_tools is not None and not isinstance(allowed_tools, Scalar):
            section.error(f"{rel}: 'allowed-tools' must be one space-separated string")

        metadata = data.get("metadata")
        if not isinstance(metadata, dict):
            section.error(
                f"{rel}: add a metadata block with 'author: {AUTHOR}' and 'version: \"X.Y.Z\"'"
            )
        else:
            for sub_key, sub in metadata.items():
                if sub.style == "plain" and NON_STRING_RE.match(sub.value):
                    section.error(
                        f"{rel}: metadata.{sub_key} would be read as a number or a yes/no "
                        f'value; put it in double quotes: {sub_key}: "{sub.value}"'
                    )
            author = metadata.get("author")
            if author is None or author.value != AUTHOR:
                section.error(f"{rel}: metadata.author must be '{AUTHOR}'")
            skill_version = metadata.get("version")
            if skill_version is None:
                section.error(f"{rel}: metadata.version is missing")
            elif version and skill_version.value != version:
                section.error(
                    f"{rel}: metadata.version is {skill_version.value!r} but {PLUGIN_JSON} "
                    f"says {version!r}",
                    "use one version everywhere: set it in plugin.json and in every "
                    "skill's metadata.version",
                )

        body = "\n".join(text.split("\n")[body_start:])
        if not body.strip():
            section.error(f"{rel}: the body after the frontmatter is empty")
        total = text.rstrip("\n").count("\n") + 1
        if total > MAX_SKILL_LINES:
            section.warn(
                f"{rel}: {total} lines; the spec advises under 500",
                "move detail into references/ files",
            )
    return section


PATH_MENTION_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:references|scripts|assets)/[A-Za-z0-9._/-]+)"
)
BARE_MENTION_RE = re.compile(r"`([A-Za-z0-9._-]+\.(?:md|py|json|txt|csv|yaml|yml))`")


def check_skill_paths(skills: list[Path]) -> Section:
    section = Section("Files mentioned inside each skill exist in that skill")
    for skill in skills:
        texts = [
            p
            for p in sorted(skill.rglob("*"))
            if p.is_file()
            and p.suffix in TEXT_SUFFIXES_IN_SKILLS
            and p.name not in ("LICENSE.txt", "NOTICE.txt")
        ]
        for path in texts:
            rel = path.relative_to(ROOT)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_no, line in enumerate(text.split("\n"), start=1):
                for match in PATH_MENTION_RE.finditer(line):
                    mention = match.group(1).rstrip(".,;:)")
                    if mention.endswith("/"):
                        continue
                    if not (skill / mention).exists():
                        section.error(
                            f"{rel}:{line_no}: mentions {mention}, which is not in {skill.name}/",
                            "add the file to the skill, or fix the path; each skill must work "
                            "on its own",
                        )
                if "../" in line:
                    section.error(
                        f"{rel}:{line_no}: points outside the skill with '../'",
                        "keep each skill self-contained; copy what it needs into its folder",
                    )
                for match in BARE_MENTION_RE.finditer(line):
                    name = match.group(1)
                    places = (skill, skill / "references", skill / "scripts", skill / "assets")
                    if not any((place / name).is_file() for place in places):
                        section.warn(
                            f"{rel}:{line_no}: mentions `{name}`, which is not in {skill.name}/"
                        )
    return section


def check_shared() -> Section:
    section = Section("Shared references in sync (shared/references/ to every skill)")
    if not sync_shared.shared_files(ROOT):
        section.error("shared/references/ is missing or empty")
        return section
    for item in sync_shared.find_drift(ROOT, kinds=("shared",)):
        section.error(
            f"{item.copy.target} {item.reason}",
            "edit the file in shared/references/, then run: python3 scripts/sync_shared.py",
        )
    return section


def check_license_copies() -> Section:
    section = Section(
        "LICENSE and NOTICE copies (each skills/*/LICENSE.txt and NOTICE.txt equal the root files)"
    )
    license_file = ROOT / "LICENSE"
    if not license_file.is_file():
        section.skipped = "no LICENSE at the repo root yet, so there is nothing to compare"
        return section
    head = license_file.read_text(encoding="utf-8", errors="replace")[:400]
    if "Apache License" not in head or "Version 2.0" not in head:
        section.error(
            "LICENSE does not look like the Apache License 2.0",
            "restore it with: gh api licenses/apache-2.0 --jq .body > LICENSE",
        )
    if not (ROOT / "NOTICE").is_file():
        section.error(
            "NOTICE is missing at the repo root",
            "restore it: it carries the MIT notice for the adapted writing rules",
        )
    for item in sync_shared.find_drift(ROOT, kinds=("license", "notice")):
        section.error(f"{item.copy.target} {item.reason}", "run: python3 scripts/sync_shared.py")
    return section


def check_hygiene(files: list[Path], tracked: set[Path], used_git: bool) -> Section:
    section = Section("Repository hygiene (symlinks, junk files, layout)")
    on_disk = walk(ROOT)
    for path in on_disk:
        if path.is_symlink():
            section.error(
                f"{path.relative_to(ROOT)} is a symlink",
                "replace symlinks with real copies; they break zips, Windows and installers",
            )
    if used_git:
        staged = run_git("ls-files", "-s") or ""
        for line in staged.splitlines():
            if line.startswith("120000 "):
                section.error(f"{line.split(chr(9), 1)[-1]} is tracked as a symlink")

    def junk_reason(rel: Path) -> str | None:
        for part in rel.parts:
            if part in JUNK_NAMES or part.startswith("._"):
                return part
        if rel.name.endswith(JUNK_SUFFIXES):
            return rel.suffix
        return None

    for rel in sorted(tracked):
        if junk_reason(rel):
            section.error(
                f"{rel} is tracked by git", f"remove it from git: git rm --cached '{rel}'"
            )
    reported: set[Path] = set()
    for path in sorted(on_disk):
        rel = path.relative_to(ROOT)
        if rel.parts[0] == "dist" or rel in tracked:
            continue
        kind = junk_reason(rel)
        if kind and not any(parent in reported for parent in rel.parents):
            reported.add(rel)
            section.error(
                f"{rel} is present outside dist/",
                "delete junk files: find . -name .DS_Store -delete; "
                "find . -name __pycache__ -prune -exec rm -rf {} +; zips belong in dist/ only",
            )

    if (ROOT / "bin").exists():
        section.error(
            "there is a top-level bin/ folder", "rename it; claude.ai refuses a plugin with bin/"
        )
    if (ROOT / "CLAUDE.md").exists():
        section.error(
            "there is a CLAUDE.md at the repo root",
            "move it to .claude/CLAUDE.md; a root CLAUDE.md fails claude plugin validate --strict",
        )
    if (ROOT / ".claude" / "skills").exists():
        section.error(
            ".claude/skills/ exists",
            "use .claude/commands/ for maintainer helpers; npx skills offers .claude/skills/ "
            "to end users",
        )
    attributes = ROOT / ".gitattributes"
    if attributes.is_file():
        for line_no, line in enumerate(attributes.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            if "export-ignore" in line or "filter=" in line:
                section.error(
                    f".gitattributes:{line_no}: no export-ignore or filter attributes",
                    "remove the attribute; plugin installs and the plugin directory need "
                    "the full tree",
                )
    if used_git:
        if LOCAL_DENYLIST in tracked:
            section.error(
                f"{LOCAL_DENYLIST} is tracked by git; it holds private terms",
                f"run: git rm --cached {LOCAL_DENYLIST}  (it must stay gitignored)",
            )
        elif (ROOT / LOCAL_DENYLIST).exists() and LOCAL_DENYLIST in files:
            section.error(
                f"{LOCAL_DENYLIST} is not gitignored", f"add {LOCAL_DENYLIST} to .gitignore"
            )
    return section


def check_spdx(files: list[Path]) -> Section:
    section = Section("License headers in Python files (SPDX-License-Identifier)")
    header = f"SPDX-License-Identifier: {LICENSE_ID}"
    for rel in files:
        if rel.suffix != ".py":
            continue
        text = read_text(rel) or ""
        if header in "\n".join(text.split("\n")[:5]):
            continue
        message = f"{rel}: no '# {header}' line in the first five lines"
        fix = f"add '# {header}' as the first line, or the second after a #! line"
        if rel.parts[0] == "skills":
            section.warn(message + " (skill content: to be added in the content update)", fix)
        else:
            section.error(message, fix)
    return section


RUFF_TOML = Path("ruff.toml")
EXCLUDE_BLOCK_RE = re.compile(r"^extend-exclude\s*=\s*\[(.*?)\]", re.MULTILINE | re.DOTALL)


def check_ruff_exclusions() -> Section:
    """Warn about every skill file that ruff.toml keeps out of the Python lint."""
    section = Section("Python lint coverage (files excluded in ruff.toml)")
    path = ROOT / RUFF_TOML
    if not path.is_file():
        section.skipped = "no ruff.toml at the repo root"
        return section
    block = EXCLUDE_BLOCK_RE.search(path.read_text(encoding="utf-8"))
    entries = re.findall(r'^\s*"([^"]+)"', block.group(1), re.MULTILINE) if block else []
    for entry in entries:
        if entry.startswith("skills/"):
            section.warn(
                f"{entry} is excluded from ruff check and ruff format "
                "(skill content: to be linted and formatted in the content update)",
                "fix the ruff findings in the file, then remove its line from extend-exclude "
                "in ruff.toml",
            )
        else:
            section.error(
                f"{entry} is excluded from ruff in ruff.toml",
                "only skill content waiting for its content update may be excluded; "
                "lint and format the file instead",
            )
    return section


def load_local_terms() -> list[tuple[str, re.Pattern[str]]]:
    path = ROOT / LOCAL_DENYLIST
    if not path.is_file():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            pattern = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)
            terms.append((term, pattern))
    return terms


def email_allowed(address: str) -> bool:
    local, _, domain = address.lower().partition("@")
    if domain.endswith(NOT_EMAIL_SUFFIXES):
        return True  # a file name such as icon@2x.png, not an address
    if address.lower() in ALLOWED_EMAILS:
        return True
    if local in ("noreply", "no-reply") or local.endswith(("+noreply", ".noreply")):
        return True
    return domain in ALLOWED_EMAIL_DOMAINS or domain.endswith(
        tuple("." + d for d in ALLOWED_EMAIL_DOMAINS)
    )


def check_public(files: list[Path]) -> tuple[Section, Section]:
    public = Section("Public-repo denylist (emails, internal links, private markings)")
    secrets = Section("Secrets (keys and tokens)")
    local_terms = load_local_terms()
    if not local_terms:
        public.notes.append(
            f"no {LOCAL_DENYLIST} found, so client names and other private terms were not "
            "checked (maintainers keep one locally; see AGENTS.md)"
        )
    scanned = 0
    for rel in files:
        if rel == LOCAL_DENYLIST or (ROOT / rel).is_symlink():
            continue
        text = read_text(rel)
        if text is None:
            continue
        scanned += 1
        posix = rel.as_posix()
        for line_no, line in enumerate(text.split("\n"), start=1):
            where = f"{posix}:{line_no}"
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    secrets.error(
                        f"{where}: looks like {label}",
                        "remove it, revoke the key, and treat it as leaked",
                    )
            if rel == DENYLIST_SELF:
                continue
            for match in EMAIL_RE.finditer(line):
                if not email_allowed(match.group(0)):
                    public.error(
                        f"{where}: email address {match.group(0)}",
                        "remove email addresses; point to https://novaforma.ai "
                        "or use a noreply address",
                    )
            for match in INTERNAL_HOST_RE.finditer(line):
                public.error(
                    f"{where}: link to an internal tool ({match.group(0)})",
                    "remove links to internal tools and documents; cite public sources only",
                )
            for match in BOI_HOST_RE.finditer(line):
                if match.group(0).lower() not in ALLOWED_BOI_HOSTS:
                    public.error(
                        f"{where}: Board of Innovation address {match.group(0)}",
                        "the only allowed addresses are https://novaforma.ai "
                        "and https://www.boardofinnovation.com",
                    )
            for match in GITHUB_ORG_RE.finditer(line):
                org, repo = match.group(1), (match.group(2) or "").rstrip(".")
                if org.lower() != PUBLIC_ORG.lower() or (
                    repo and repo.removesuffix(".git").lower() != PUBLIC_REPO
                ):
                    public.error(
                        f"{where}: link to another GitHub repo or org ({match.group(0).rstrip('.')})",
                        f"link only to github.com/{PUBLIC_ORG}/{PUBLIC_REPO}",
                    )
            marking = PRIVATE_MARKING_RE.search(line) or CAPS_CONFIDENTIAL_RE.search(line)
            if not marking and not posix.startswith(RULE_FILES):
                marking = CONFIDENTIAL_RE.search(line)
            if marking and not any(
                posix == path and phrase in line for path, phrase in REVIEWED_ALLOW
            ):
                public.error(
                    f"{where}: the words '{marking.group(0)}' suggest private material",
                    "rephrase or remove it; if a maintainer has checked the line is fine to "
                    "publish, add the path and line to REVIEWED_ALLOW in scripts/check.py",
                )
            for term, pattern in local_terms:
                if pattern.search(line):
                    public.error(
                        f"{where}: matches a private term from {LOCAL_DENYLIST} ({term})",
                        "remove it; replace real names and figures with invented, obviously "
                        "illustrative ones",
                    )
    if scanned == 0:
        public.error("no text files were scanned")
    return public, secrets


def main() -> int:
    skills = sync_shared.skill_dirs(ROOT)
    files, tracked, used_git = repo_files()

    manifests, version = check_manifests()
    sections = [
        check_frontmatter(skills, version),
        check_skill_paths(skills),
        check_shared(),
        check_license_copies(),
        manifests,
        check_hygiene(files, tracked, used_git),
        check_spdx(files),
        check_ruff_exclusions(),
        *check_public(files),
    ]

    print("Nova Forma repository checks")
    print(f"{len(skills)} skills, {len(files)} files" + ("" if used_git else " (git not found)"))
    print()
    for section in sections:
        section.show()
    errors = sum(len(s.errors) for s in sections)
    warnings = sum(len(s.warnings) for s in sections)
    print()
    if errors:
        print(f"FAILED: {errors} error(s), {warnings} warning(s). Fix the errors above.")
        return 1
    print(f"OK: all checks passed, {warnings} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
