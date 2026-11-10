#!/usr/bin/env python3
"""Validate the skill package. Standard library only.

Checks: SKILL.md frontmatter, size, relative Markdown links, files named in
SKILL.md, SVG well-formedness, Python syntax, and obvious committed secrets.
Use --check-external to also test http(s) links (needs network).
"""
import argparse
import re
import sys
import xml.dom.minidom
import py_compile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SECRET_RE = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
SKIP_DIRS = {".git", "__pycache__", "node_modules"}


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with '---' frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "frontmatter is not closed with '---'"
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if ":" not in line:
            return None, "invalid frontmatter line: %r" % line
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip().strip("\"'")
    return data, None


def iter_files(suffixes):
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in suffixes and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def check_skill_md(errors):
    path = ROOT / "SKILL.md"
    if not path.exists():
        errors.append("SKILL.md is missing")
        return
    text = path.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        errors.append(err)
        return
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append("name must be lowercase letters, digits and hyphens, max 64 chars (got %r)" % name)
    if not desc:
        errors.append("description is required")
    elif len(desc) > 1024:
        errors.append("description is %d chars; max is 1024" % len(desc))
    if "<" in desc or ">" in desc:
        errors.append("description must not contain angle brackets")
    extra = set(fm) - {"name", "description", "license", "compatibility", "allowed-tools", "metadata"}
    if extra:
        errors.append("unexpected frontmatter keys: %s" % ", ".join(sorted(extra)))
    if text.count("\n") > 500:
        errors.append("SKILL.md is over 500 lines; move detail into references/")
    for ref in re.findall(r"`((?:references|examples|scripts|docs|assets)/[A-Za-z0-9_./-]+)`", text):
        if not (ROOT / ref).exists():
            errors.append("SKILL.md mentions %s but it does not exist" % ref)


def check_links(errors, external):
    for md in iter_files({".md"}):
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("mailto:", "#")):
                continue
            if target.startswith(("http://", "https://")):
                if external:
                    try:
                        req = urllib.request.Request(target, headers={"User-Agent": "ownlyplans-skill-validate"})
                        urllib.request.urlopen(req, timeout=15).close()
                    except Exception as exc:  # noqa: BLE001
                        errors.append("%s: external link failed %s (%s)" % (md.relative_to(ROOT), target, exc))
                continue
            rel = target.split("#")[0]
            if rel and not (md.parent / rel).resolve().exists():
                errors.append("%s: broken link %s" % (md.relative_to(ROOT), target))


def check_svgs(errors):
    for svg in iter_files({".svg"}):
        try:
            xml.dom.minidom.parse(str(svg))
        except Exception as exc:  # noqa: BLE001
            errors.append("%s: invalid SVG (%s)" % (svg.relative_to(ROOT), exc))


def check_python(errors):
    for py in iter_files({".py"}):
        try:
            py_compile.compile(str(py), cfile=tempfile.mktemp(suffix=".pyc"), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append("%s: syntax error (%s)" % (py.relative_to(ROOT), exc.msg))


def check_secrets(errors):
    for p in ROOT.rglob("*"):
        if not p.is_file() or set(p.relative_to(ROOT).parts) & SKIP_DIRS or p.suffix in {".png", ".zip"}:
            continue
        if p.name == ".env" or p.name.startswith(".env."):
            errors.append("%s: .env files must not be committed" % p.relative_to(ROOT))
            continue
        if p.name in {"validate_skill.py", "test_skill.py"}:
            continue
        try:
            if SECRET_RE.search(p.read_text(encoding="utf-8")):
                errors.append("%s: looks like it contains a secret" % p.relative_to(ROOT))
        except UnicodeDecodeError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-external", action="store_true")
    args = ap.parse_args()
    errors = []
    check_skill_md(errors)
    check_links(errors, args.check_external)
    check_svgs(errors)
    check_python(errors)
    check_secrets(errors)
    if errors:
        print("FAILED (%d problem%s):" % (len(errors), "" if len(errors) == 1 else "s"))
        for e in errors:
            print(" - " + e)
        return 1
    print("OK: skill package is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
