"""Generate a markdown report from dry-run output."""

import json
import sys
from pathlib import Path


def generate_report(output_dir: Path, report_path: Path | None = None) -> Path:
    """Read dry-run output files and produce a markdown report."""
    hints = json.loads((output_dir / "hints.json").read_text())
    rule_candidates = json.loads((output_dir / "rule_candidates.json").read_text())
    metadata = {}
    metadata_path = output_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text())

    if report_path is None:
        report_path = output_dir / "report.md"

    lines: list[str] = []
    _migration_section(lines, metadata)
    _summary_section(lines, hints, rule_candidates, metadata)
    _rules_section(lines, rule_candidates)
    _hints_section(lines, hints)

    report_path.write_text("\n".join(lines))
    return report_path


def _migration_section(lines: list[str], metadata: dict) -> None:
    desc = metadata.get("migration_description", "Not available")
    inferred = metadata.get("inferred", False)
    source_label = "Inferred from manifest diffs" if inferred else "Provided by user"
    targets = metadata.get("target_labels", [])
    sources = metadata.get("source_labels", [])

    lines.append("# KAI Commit Miner Report")
    lines.append("")
    lines.append(f"**Migration** ({source_label}): {desc}")
    lines.append("")
    if sources:
        lines.append(f"**Source labels:** {', '.join(sources)}")
    if targets:
        lines.append(f"**Target labels:** {', '.join(targets)}")
    if sources or targets:
        lines.append("")
    label_selector = metadata.get("label_selector", "")
    if label_selector:
        lines.append(f"**Label selector:** `{label_selector}`")
        lines.append("")


def _summary_section(
    lines: list[str], hints: list, rules: list, metadata: dict
) -> None:
    violations_resolved = metadata.get("violations_resolved", 0)
    files_changed = metadata.get("files_changed", 0)
    generated = sum(1 for h in hints if not h.get("skipped"))
    skipped = sum(1 for h in hints if h.get("skipped"))
    violation_types = len(
        {
            f"{h['violation_key']['ruleset_name']}/{h['violation_key']['violation_name']}"
            for h in hints
        }
    )

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Violations resolved | {violations_resolved} |")
    lines.append(f"| Files changed | {files_changed} |")
    lines.append(f"| Violation types | {violation_types} |")
    lines.append(f"| Hints generated | {generated} |")
    lines.append(f"| Hints skipped | {skipped} |")
    lines.append(f"| New rules discovered | {len(rules)} |")
    lines.append("")


def _rules_section(lines: list[str], rules: list) -> None:
    if not rules:
        lines.append("## New Rule Candidates")
        lines.append("")
        lines.append("None discovered.")
        lines.append("")
        return

    high = [r for r in rules if str(r.get("migration_relevance", "")).lower() == "high"]
    other = [
        r for r in rules if str(r.get("migration_relevance", "")).lower() != "high"
    ]

    lines.append(f"## New Rule Candidates ({len(rules)})")
    lines.append("")
    lines.append(
        f"Proposed analyzer-lsp rules detecting pre-migration patterns. "
        f"{len(high)} high-relevance, {len(other)} lower."
    )
    lines.append("")

    for r in rules:
        relevance = str(r.get("migration_relevance", "medium")).lower()
        rule_id = r.get("ruleID", "unknown")
        desc = r.get("description", "")
        reasoning = r.get("relevance_reasoning", "")
        validation = r.get("validation_notes", [])

        lines.append(f"### `{rule_id}` — {relevance}")
        lines.append("")
        lines.append(f"**{desc}**")
        lines.append("")
        if reasoning:
            lines.append(f"> {reasoning}")
            lines.append("")
        if validation:
            lines.append(f"**Warnings:** {', '.join(validation)}")
            lines.append("")

        # Reconstruct the rule YAML
        rule_yaml = f"- ruleID: {rule_id}\n"
        rule_yaml += f"  description: {desc}\n"
        rule_yaml += f"  category: {r.get('category', 'potential')}\n"
        rule_yaml += f"  effort: {r.get('effort', 1)}\n"
        if r.get("when_yaml"):
            rule_yaml += "  when:\n"
            for line in r["when_yaml"].split("\n"):
                rule_yaml += f"    {line}\n"
        if r.get("message"):
            rule_yaml += "  message: |\n"
            for line in r["message"].split("\n"):
                rule_yaml += f"    {line}\n"
        if r.get("labels"):
            rule_yaml += "  labels:\n"
            for label in r["labels"]:
                rule_yaml += f"    - {label}\n"

        lines.append("```yaml")
        lines.append(rule_yaml.rstrip())
        lines.append("```")
        lines.append("")


def _hints_section(lines: list[str], hints: list) -> None:
    # Group by violation type
    by_violation: dict[str, list[dict]] = {}
    for h in hints:
        key = f"{h['violation_key']['ruleset_name']} / {h['violation_key']['violation_name']}"
        by_violation.setdefault(key, []).append(h)

    generated = [h for h in hints if not h.get("skipped")]
    skipped = [h for h in hints if h.get("skipped")]

    lines.append(f"## Hints ({len(generated)} generated, {len(skipped)} skipped)")
    lines.append("")

    for key in sorted(by_violation.keys()):
        group = by_violation[key]
        total_incidents = sum(h.get("incident_count", 1) for h in group)
        skipped_count = sum(1 for h in group if h.get("skipped"))

        lines.append(f"### {key}")
        lines.append(f"*{total_incidents} incidents, {skipped_count} skipped*")
        lines.append("")

        for h in group:
            if h.get("skipped"):
                reason = h.get("skipped_reason", "")
                lines.append(f"<details><summary>Skipped: {reason[:80]}</summary>")
                lines.append("")
                lines.append(f"{reason}")
                lines.append("")
                lines.append("</details>")
                lines.append("")
                continue

            hint_text = h.get("hint_text", "")
            # Strip markdown code fences if the LLM wrapped the output
            if hint_text.startswith("```"):
                hint_lines = hint_text.split("\n")
                hint_text = "\n".join(l for l in hint_lines if not l.startswith("```"))

            lines.append(hint_text.strip())
            lines.append("")

            # Show sample files
            for sf in h.get("sample_files", []):
                file_path = sf.get("file_path", "")
                before = sf.get("before_snippet", "")
                after = sf.get("after_snippet", "")
                if before or after:
                    lines.append(
                        f"<details><summary><code>{file_path}</code></summary>"
                    )
                    lines.append("")
                    if before:
                        lines.append("Before:")
                        lines.append("```")
                        lines.append(before[:300])
                        lines.append("```")
                    if after:
                        lines.append("After:")
                        lines.append("```")
                        lines.append(after[:300])
                        lines.append("```")
                    lines.append("</details>")
                    lines.append("")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m kai_commit_miner.report <output_dir> [report.md]",
            file=sys.stderr,
        )
        sys.exit(1)
    output_dir = Path(sys.argv[1])
    report_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    path = generate_report(output_dir, report_path)
    print(f"Report written to {path}")
