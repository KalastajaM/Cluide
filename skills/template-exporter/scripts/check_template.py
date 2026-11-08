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
LEGACY_MARKER = re.compile(r"<<<\s*PLACEHOLDER")
RUNTIME_NAMES = {"run_log.md", "improvements.md", ".env", ".ds_store", "thumbs.db",
                 "settings.local.json", "identifiers.txt"}
RUNTIME_SUFFIXES = (".log",)
RUNTIME_DIRS = {".git", "__pycache__", "node_modules", "memory", "outputs", "logs"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh", ".js", ".ts",
                 ".html", ".csv", ".xml", ".ini", ".cfg", ""}


def placeholder_key(body):
    """Description part of a placeholder, before any EXAMPLE clause."""
    return re.split(r"\s*(?:—|--|-)?\s*EXAMPLE\s*:", body, maxsplit=1, flags=re.I)[0].strip().strip('"').lower()


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
        parts = {x.lower() for x in p.relative_to(root).parts[:-1]}
        if p.name.lower() in RUNTIME_NAMES or p.name.lower().endswith(RUNTIME_SUFFIXES) or parts & RUNTIME_DIRS:
            add("HIGH", rel, "runtime-state or private file should not ship in a template")
        if p.suffix.lower() not in TEXT_SUFFIXES:
            add("MEDIUM", rel, "binary or unknown file type: inspect by hand for identifying content")
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
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
                add("MEDIUM", loc, "legacy <<<PLACEHOLDER>>> marker: use [PLACEHOLDER: ...] everywhere")
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
