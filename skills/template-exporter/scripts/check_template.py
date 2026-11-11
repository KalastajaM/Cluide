#!/usr/bin/env python3
"""Scan an exported template folder for leaks and structural gaps, then optionally zip it.

Part of the template-exporter skill. Python 3.8+ standard library only.

Usage:
    python3 check_template.py TEMPLATE_DIR [--identifiers FILE] [--zip]

Exit codes: 0 = no HIGH findings, 1 = HIGH findings, 2 = usage error.
Secrets are reported by location and kind only, never by value.
"""
import argparse
import re
import sys
import zipfile
from pathlib import Path

SECRET_PATTERNS = [
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}")),
    ("OpenAI-style API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Credentials in URL", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^\s/:@]+:[^\s/@]+@", re.I)),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9_\-.=]{20,}")),
    ("Assigned secret", re.compile(
        r"\b(?:api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"]?(?!\[PLACEHOLDER)[^\s'\"\[]{8,}", re.I)),
]
EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@([A-Za-z0-9.\-]+\.[A-Za-z]{2,})\b")
SAFE_EMAIL_DOMAINS = re.compile(r"(?:^|\.)example\.(?:com|org|net)$|(?:^|\.)(?:example|test|invalid|localhost)$", re.I)
PERSONAL_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)([A-Za-z0-9._\-]+)")
SAFE_PATH_USERS = {"you", "your-name", "yourname", "username", "user", "name", "me", "example", "[placeholder"}
PLACEHOLDER = re.compile(r"\[PLACEHOLDER:\s*([^\]]*?)\s*\]")
LEGACY_MARKER = re.compile(r"<<<[^>\n]{1,80}>>>|<<<\s*PLACEHOLDER")
RUNTIME_NAMES = {".env", ".ds_store", "thumbs.db", "settings.local.json", "identifiers.txt"}
RUNTIME_SUFFIXES = (".log",)
RUNTIME_DIRS = {".git", "__pycache__", "node_modules", "memory", ".memory", "auto-memory", ".auto-memory"}
# State files and folders a template may legitimately ship as an empty starting definition:
# HIGH only when they hold run data (see starting_state), otherwise MEDIUM.
SCAFFOLD_NAMES = {"run_log.md", "improvements.md"}
# Key-name examples are safe to ship by name; their content is still scanned like any other file.
ENV_EXAMPLES = {".env.example", ".env.sample", ".env.template", ".env.dist"}
SCAFFOLD_DIRS = {"outputs", "logs"}
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
RUN_DATA = re.compile(
    r"\b(?:19|20)\d\d[-/.](?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12]\d|3[01])\b"   # a real calendar date
    r"|\b(?:19|20)\d\d(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\b"            # YYYYMMDD
    r"|\"total_runs\"\s*:\s*[1-9]")                                           # a non-zero run counter


def placeholder_key(body):
    """Description part of a placeholder, before any EXAMPLE clause."""
    return re.split(r"\s*(?:—|--|-)?\s*EXAMPLE\s*:", body, maxsplit=1, flags=re.I)[0].strip().strip('"').lower()


def starting_state(name, text, folder_note):
    """True if a state file is an empty starting definition rather than live run data.

    Headings, blank lines and HTML comments alone always qualify. A run log, improvements file or
    folder note (README.md under outputs/logs) also qualifies when it holds no real dates and no
    non-zero run counter, so the shipped task and project scaffolds pass. Anything else does not.
    """
    lines = [l.strip() for l in HTML_COMMENT.sub("", text).splitlines() if l.strip()]
    if all(l.startswith("#") for l in lines):
        return True
    if name in SCAFFOLD_NAMES or folder_note:
        return not RUN_DATA.search(HTML_COMMENT.sub("", text))
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template_dir", type=Path)
    ap.add_argument("--identifiers", type=Path, help="file with one identifying string per line (kept outside the template)")
    ap.add_argument("--zip", action="store_true", help="write <dir>.zip beside the folder if no HIGH findings")
    args = ap.parse_args()

    root = args.template_dir.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    identifiers = []
    if args.identifiers:
        if not args.identifiers.is_file():
            print(f"error: identifiers file {args.identifiers} not found", file=sys.stderr)
            return 2
        if root in args.identifiers.resolve().parents:
            print("error: identifiers file must live outside the template folder", file=sys.stderr)
            return 2
        identifiers = [l.strip() for l in args.identifiers.read_text(encoding="utf-8").splitlines()
                       if l.strip() and not l.lstrip().startswith("#")]

    findings = []  # (severity, location, message)

    def add(sev, loc, msg):
        findings.append((sev, loc, msg))

    files = sorted(p for p in root.rglob("*") if p.is_file())
    placeholders = {}  # key -> list of locations
    readme_text = ""

    for p in files:
        rel = p.relative_to(root).as_posix()
        name = p.name.lower()
        parts = {x.lower() for x in p.relative_to(root).parts[:-1]}
        in_scaffold_dir = bool(parts & SCAFFOLD_DIRS)
        data = p.read_bytes()
        binary = b"\0" in data[:8192]  # a NUL byte in the first 8 KB: a real binary, not text
        text = None
        if not binary:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                pass
        if name == ".env" or (name.startswith(".env.") and name not in ENV_EXAMPLES):
            add("HIGH", rel, "environment file (.env*) holds live secrets and must not ship in a template")
        elif (name in RUNTIME_NAMES or parts & RUNTIME_DIRS
              or (name.endswith(RUNTIME_SUFFIXES) and not in_scaffold_dir)):
            add("HIGH", rel, "runtime-state or private file should not ship in a template")
        elif name in SCAFFOLD_NAMES or in_scaffold_dir:
            if text is not None and starting_state(name, text, name == "readme.md" and in_scaffold_dir):
                add("MEDIUM", rel, "starting-state file: confirm it is empty of run data")
            else:
                add("HIGH", rel, "runtime-state or private file should not ship in a template")
        if binary:
            add("MEDIUM", rel, "binary file: inspect by hand for identifying content")
            continue
        if text is None:
            add("MEDIUM", rel, "not UTF-8 text: inspect by hand")
            continue
        if p.name.lower() == "readme.md" and p.parent == root:
            readme_text = text.lower()

        for n, line in enumerate(text.splitlines(), 1):
            loc = f"{rel}:{n}"
            for kind, rx in SECRET_PATTERNS:
                if rx.search(line):
                    add("HIGH", loc, f"possible secret ({kind}); value not shown")
            for m in EMAIL.finditer(line):
                if not SAFE_EMAIL_DOMAINS.search(m.group(1)):
                    add("HIGH", loc, f"email address on non-example domain: {m.group(0)}")
            for m in PERSONAL_PATH.finditer(line):
                if m.group(1).lower() not in SAFE_PATH_USERS:
                    add("HIGH", loc, f"personal absolute path: {m.group(0)}")
            low = line.lower()
            for ident in identifiers:
                if ident.lower() in low:
                    add("HIGH", loc, f"identifier from list: {ident!r}")
            if LEGACY_MARKER.search(line):
                add("MEDIUM", loc, "leftover <<<...>>> marker: use [PLACEHOLDER: ...] everywhere")
            for m in PLACEHOLDER.finditer(line):
                body = m.group(1)
                if not re.search(r"EXAMPLE\s*:", body, re.I):
                    add("MEDIUM", loc, f"placeholder without EXAMPLE: [PLACEHOLDER: {body}]")
                placeholders.setdefault(placeholder_key(body), []).append(loc)

        if p.name == "SKILL.md":
            fm = re.match(r"---\n(.*?)\n---", text, re.S)
            if not fm:
                add("HIGH", rel, "SKILL.md has no YAML frontmatter")
            else:
                d = re.search(r"^description:\s*(>[-+]?|\|[-+]?)?\s*\n?((?:.*\n?)*?)(?=^\S|\Z)", fm.group(1), re.M)
                desc = " ".join(d.group(2).split()) if d else ""
                if not desc:
                    add("HIGH", rel, "SKILL.md frontmatter has no description")
                elif len(desc) > 1024:
                    add("MEDIUM", rel, f"description is {len(desc)} characters; keep within 1024 to install everywhere")

    for required in ("README.md", "SETUP.md"):
        if not (root / required).is_file():
            add("HIGH", required, "required file missing")
    if readme_text:
        for key, locs in sorted(placeholders.items()):
            if key and key not in readme_text and not all(l.startswith("README.md") for l in locs):
                add("MEDIUM", locs[0], f"placeholder not described in README: {key!r} ({len(locs)} use(s))")

    order = {"HIGH": 0, "MEDIUM": 1}
    findings.sort(key=lambda f: (order[f[0]], f[1]))
    for sev, loc, msg in findings:
        print(f"{sev:6} {loc}  {msg}")
    highs = sum(1 for f in findings if f[0] == "HIGH")
    print(f"\n{len(files)} files scanned, {len(placeholders)} distinct placeholders, "
          f"{highs} HIGH, {len(findings) - highs} MEDIUM")

    if highs:
        if args.zip:
            print("zip not written: fix HIGH findings first")
        return 1

    if args.zip:
        out = root.parent / f"{root.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(p, Path(root.name) / p.relative_to(root))
        with zipfile.ZipFile(out) as z:
            bad = z.testzip()
            names = z.namelist()
        if bad or len(names) != len(files):
            print(f"error: archive check failed ({bad or 'file count mismatch'})", file=sys.stderr)
            return 1
        print(f"wrote {out} ({len(names)} files, verified)")
        for name in names:
            print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
