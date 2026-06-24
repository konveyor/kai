#!/usr/bin/env python3
"""Prompt template governance checks (ISO 42001 A.5.2).

Validates the versioned prompt template set under
``src/kai_mcp_solution_server/prompts/``:

  - every ``.jinja`` template is declared in ``manifest.yaml`` (and vice-versa)
  - content checksums in the manifest match the files on disk (drift detection)
  - every template parses as Jinja2 (syntactic verification)
  - declared variables exactly match the template's referenced variables, and no
    leftover ``{var}`` f-string interpolation escaped into a template asset

Usage:
  python scripts/prompts_version.py check     # CI gate (non-zero exit on problems)
  python scripts/prompts_version.py update    # recompute + write checksums
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, meta

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "src" / "kai_mcp_solution_server" / "prompts"
TEMPLATES_DIR = PROMPTS_DIR / "templates"
MANIFEST_PATH = PROMPTS_DIR / "manifest.yaml"

# Matches a leftover Python f-string placeholder like ``{incident.uri}`` while
# ignoring Jinja's own ``{{ ... }}`` / ``{% ... %}``.
_FSTRING_RE = re.compile(r"(?<!\{)\{[A-Za-z_][\w.]*\}(?!\})")


def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def check() -> int:
    manifest = load_manifest()
    templates = manifest.get("templates", [])
    problems: list[str] = []
    env = Environment()  # noqa: S701  # nosec B701 - parses templates, never renders

    on_disk = {p.relative_to(ROOT).as_posix() for p in TEMPLATES_DIR.rglob("*.jinja")}
    declared = {t["path"] for t in templates}
    for path in on_disk - declared:
        problems.append(f"Template on disk is not declared in manifest.yaml: {path}")
    for path in declared - on_disk:
        problems.append(
            f"Manifest declares a template that does not exist on disk: {path}"
        )

    for entry in templates:
        abs_path = ROOT / entry["path"]
        if not abs_path.exists():
            continue  # missing-file already reported
        src = abs_path.read_text()

        actual = sha256(src)
        if entry.get("checksum") != actual:
            problems.append(
                f"Checksum drift for {entry['id']} ({entry['path']}). "
                f"Manifest: {entry.get('checksum') or '<none>'}, actual: {actual}. "
                'Run "python scripts/prompts_version.py update" and review the change.'
            )

        try:
            ast = env.parse(src)
        except Exception as err:  # noqa: BLE001 - report any parse failure
            problems.append(
                f"Jinja2 parse error in {entry['id']} ({entry['path']}): {err}"
            )
            continue

        if _FSTRING_RE.search(src):
            problems.append(
                f"Leftover {{...}} f-string interpolation found in {entry['id']} ({entry['path']})."
            )

        referenced = meta.find_undeclared_variables(ast)
        declared_vars = set(entry.get("variables", []))
        for missing in declared_vars - referenced:
            problems.append(
                f'Declared variable "{missing}" is not referenced in {entry["id"]} ({entry["path"]}).'
            )
        for undeclared in referenced - declared_vars:
            problems.append(
                f'Variable "{undeclared}" is used in {entry["id"]} ({entry["path"]}) '
                "but not declared in manifest.yaml."
            )

    if problems:
        print("Prompt template validation FAILED:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(f"\n{len(problems)} problem(s) found.", file=sys.stderr)
        return 1

    print(
        f"Prompt template validation passed. version={manifest.get('version')}, "
        f"templates={len(templates)}."
    )
    return 0


def update() -> int:
    manifest = load_manifest()
    for entry in manifest.get("templates", []):
        entry["checksum"] = sha256((ROOT / entry["path"]).read_text())
    header = (
        "# Prompt template manifest — governed under ISO 42001 A.5.2.\n"
        "# Checksums are maintained by scripts/prompts_version.py; do not edit by hand.\n"
    )
    MANIFEST_PATH.write_text(
        header + yaml.safe_dump(manifest, sort_keys=False, width=1000)
    )
    print(f"Updated checksums for {len(manifest.get('templates', []))} template(s).")
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        return check()
    if cmd == "update":
        return update()
    print("Usage: python scripts/prompts_version.py <check|update>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
