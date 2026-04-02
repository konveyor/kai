"""Generate an interactive HTML report from dry-run output."""

import html
import json
import sys
from pathlib import Path


def generate_html_report(output_dir: Path, report_path: Path | None = None) -> Path:
    """Read dry-run output files and produce an HTML report."""
    hints = json.loads((output_dir / "hints.json").read_text())
    rule_candidates = json.loads((output_dir / "rule_candidates.json").read_text())
    metadata = {}
    metadata_path = output_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text())

    if report_path is None:
        report_path = output_dir / "report.html"

    # Group hints by violation type
    hints_by_violation: dict[str, list[dict]] = {}
    for h in hints:
        key = f"{h['violation_key']['ruleset_name']} / {h['violation_key']['violation_name']}"
        hints_by_violation.setdefault(key, []).append(h)

    parts: list[str] = []
    parts.append(_header())
    parts.append(_migration_section(metadata))
    parts.append(_summary(hints, rule_candidates, metadata))
    parts.append(_violations_section(hints_by_violation))
    parts.append(_rule_candidates_section(rule_candidates))
    parts.append(_hints_detail_section(hints_by_violation))
    parts.append(_footer())

    report_path.write_text("\n".join(parts))
    return report_path


def _esc(text: str) -> str:
    return html.escape(text)


def _header() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>KAI Commit Miner Report</title>
<style>
  :root { --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9;
          --text2: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149;
          --yellow: #d29922; --code-bg: #1c2128; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.6; padding: 24px; max-width: 1200px; margin: 0 auto; }
  h1 { color: #fff; margin-bottom: 8px; }
  h2 { color: #fff; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  h3 { color: var(--accent); margin: 16px 0 8px; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .stats { display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0; }
  .stat { background: var(--card); border: 1px solid var(--border); border-radius: 6px;
          padding: 16px 24px; min-width: 150px; }
  .stat-value { font-size: 28px; font-weight: 600; color: #fff; }
  .stat-label { color: var(--text2); font-size: 13px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 6px;
          padding: 16px; margin: 8px 0; }
  .card-header { display: flex; justify-content: space-between; align-items: center; cursor: pointer; }
  .card-header:hover { color: var(--accent); }
  .badge { background: var(--border); color: var(--text); padding: 2px 8px; border-radius: 12px;
           font-size: 12px; font-weight: 500; }
  .badge-green { background: #23352b; color: var(--green); }
  .badge-yellow { background: #2d2a1e; color: var(--yellow); }
  .badge-red { background: #3d1f20; color: var(--red); }
  .hint-text { background: var(--code-bg); border: 1px solid var(--border); border-radius: 6px;
               padding: 16px; margin: 8px 0; white-space: pre-wrap; font-family: 'SF Mono', Consolas, monospace;
               font-size: 13px; line-height: 1.5; }
  .diff { background: var(--code-bg); border: 1px solid var(--border); border-radius: 6px;
          padding: 12px; margin: 8px 0; font-family: 'SF Mono', Consolas, monospace; font-size: 12px;
          overflow-x: auto; }
  .diff-add { color: var(--green); }
  .diff-del { color: var(--red); }
  .collapsible { display: none; }
  .collapsible.open { display: block; }
  table { width: 100%; border-collapse: collapse; margin: 8px 0; }
  th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border); }
  th { color: var(--text2); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
  .file-path { color: var(--accent); font-family: monospace; font-size: 13px; }
  .commit { font-family: monospace; color: var(--yellow); }
  nav { position: sticky; top: 0; background: var(--bg); padding: 12px 0; z-index: 10;
        border-bottom: 1px solid var(--border); margin-bottom: 16px; }
  nav a { margin-right: 16px; font-weight: 500; }
  .search { width: 100%; padding: 8px 12px; background: var(--code-bg); border: 1px solid var(--border);
            border-radius: 6px; color: var(--text); font-size: 14px; margin: 8px 0; }
  .search:focus { outline: none; border-color: var(--accent); }
  .hidden { display: none !important; }
</style>
</head>
<body>
<h1>KAI Commit Miner Report</h1>
<nav>
  <a href="#migration">Migration</a>
  <a href="#summary">Summary</a>
  <a href="#violations">Violations</a>
  <a href="#rules">New Rules</a>
  <a href="#hints">All Hints</a>
</nav>"""


def _migration_section(metadata: dict) -> str:
    desc = metadata.get("migration_description", "Not available")
    inferred = metadata.get("inferred", False)
    source_label = "Inferred from manifest diffs" if inferred else "Provided by user"
    targets = metadata.get("target_labels", [])
    sources = metadata.get("source_labels", [])

    labels_html = ""
    if targets or sources:
        labels_html = '<p style="margin-top:8px;font-size:13px">'
        if sources:
            labels_html += f'<span style="color:var(--text2)">Source:</span> {", ".join(_esc(s) for s in sources)} '
        if targets:
            labels_html += f'<span style="color:var(--text2)">Target:</span> {", ".join(_esc(t) for t in targets)}'
        labels_html += "</p>"

    return f"""
<div id="migration">
<h2>Migration</h2>
<div class="card">
  <p style="color:var(--text2);font-size:12px;margin-bottom:8px">{_esc(source_label)}</p>
  <p>{_esc(str(desc))}</p>
  {labels_html}
</div>
</div>"""


def _summary(hints: list, rules: list, metadata: dict) -> str:
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

    return f"""
<div id="summary">
<h2>Summary</h2>
<div class="stats">
  <div class="stat"><div class="stat-value">{violations_resolved}</div><div class="stat-label">Violations Resolved</div></div>
  <div class="stat"><div class="stat-value">{files_changed}</div><div class="stat-label">Files Changed</div></div>
  <div class="stat"><div class="stat-value">{violation_types}</div><div class="stat-label">Violation Types</div></div>
  <div class="stat"><div class="stat-value">{generated}</div><div class="stat-label">Hints Generated</div></div>
  <div class="stat"><div class="stat-value">{skipped}</div><div class="stat-label">Hints Skipped</div></div>
  <div class="stat"><div class="stat-value">{len(rules)}</div><div class="stat-label">New Rules</div></div>
</div>
</div>"""


def _violations_section(hints_by_violation: dict) -> str:
    cards = ""
    for key in sorted(hints_by_violation.keys()):
        group = hints_by_violation[key]
        count = len(group)
        sample = group[0]
        text_preview = sample["hint_text"][:200].replace("\n", " ")
        total_incidents = sum(h.get("incident_count", 1) for h in group)
        skipped_count = sum(1 for h in group if h.get("skipped"))

        cards += f"""
<div class="card violation-card" data-search="{_esc(key.lower())}">
  <div class="card-header" onclick="this.nextElementSibling.classList.toggle('open')">
    <h3>{_esc(key)}</h3>
    <span class="badge">{total_incidents} incidents</span>
  </div>
  <div class="collapsible">
    <p style="color:var(--text2);margin:8px 0">{_esc(text_preview)}...</p>
    <div class="hint-text">{_esc(sample["hint_text"])}</div>
    <p style="color:var(--text2);margin-top:8px;font-size:12px">{count} hint(s), {skipped_count} skipped</p>
  </div>
</div>"""

    return f"""
<div id="violations">
<h2>Violations ({len(hints_by_violation)} types)</h2>
<input class="search" type="text" placeholder="Filter violations..." oninput="filterCards(this.value, 'violation-card')">
{cards}
</div>"""


def _rule_candidates_section(rules: list) -> str:
    if not rules:
        return '<div id="rules"><h2>New Rule Candidates</h2><p style="color:var(--text2)">None discovered.</p></div>'

    _RELEVANCE_BADGES = {
        "high": "badge-green",
        "medium": "badge-yellow",
        "low": "badge-red",
        "very_low": "badge-red",
    }

    cards = ""
    for r in rules:
        relevance = str(r.get("migration_relevance", "medium")).lower()
        badge_class = _RELEVANCE_BADGES.get(relevance, "badge-yellow")

        # Reconstruct analyzer-lsp YAML
        rule_yaml = f"- ruleID: {r.get('ruleID', 'mined-unknown')}\n"
        rule_yaml += f"  description: {r.get('description', '')}\n"
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

        relevance_class = "high-relevance" if relevance == "high" else "low-relevance"
        validation = r.get("validation_notes", [])
        validation_html = ""
        if validation:
            validation_html = (
                '<p style="color:var(--yellow);font-size:12px;margin:4px 0">Warnings: '
                + ", ".join(_esc(n) for n in validation)
                + "</p>"
            )

        cards += f"""
<div class="card rule-card {relevance_class}" data-relevance="{relevance}" data-search="{_esc(r.get('description','').lower())} {_esc(r.get('ruleID','').lower())}">
  <div class="card-header" onclick="this.nextElementSibling.classList.toggle('open')">
    <h3><code>{_esc(r.get("ruleID", ""))}</code> {_esc(r.get("description", "")[:70])}</h3>
    <span class="badge {badge_class}">{relevance}</span>
  </div>
  <div class="collapsible">
    {validation_html}
    {f'<p style="color:var(--text2);margin:4px 0"><strong>Relevance:</strong> {_esc(r.get("relevance_reasoning",""))}</p>' if r.get("relevance_reasoning") else ''}
    <p style="font-size:12px;color:var(--text2)">Source: <span class="file-path">{_esc(r.get("source_file",""))}</span> @ <span class="commit">{_esc(r.get("source_commit","")[:8])}</span></p>
    <div class="hint-text">{_esc(rule_yaml)}</div>
  </div>
</div>"""

    high_rel = sum(
        1 for r in rules if str(r.get("migration_relevance", "")).lower() == "high"
    )
    return f"""
<div id="rules">
<h2>New Rule Candidates ({len(rules)})</h2>
<p style="color:var(--text2);margin-bottom:12px">Proposed analyzer-lsp rules detecting pre-migration patterns. {high_rel} high-relevance, {len(rules) - high_rel} lower.</p>
<label style="color:var(--text2);font-size:13px"><input type="checkbox" onchange="toggleLowRelevance(this.checked)" checked> Show low-relevance candidates</label>
{cards}
</div>"""


def _hints_detail_section(hints_by_violation: dict) -> str:
    rows = ""
    total = 0
    for key in sorted(hints_by_violation.keys()):
        for h in hints_by_violation[key]:
            total += 1
            skipped = h.get("skipped", False)
            incident_count = h.get("incident_count", 1)

            # Build sample files display
            samples_html = ""
            for sf in h.get("sample_files", []):
                snippet_before = _esc(sf.get("before_snippet", "")[:120])
                snippet_after = _esc(sf.get("after_snippet", "")[:120])
                diff_html = ""
                if snippet_before or snippet_after:
                    before_lines = "".join(
                        f'<div class="diff-del">- {line}</div>'
                        for line in snippet_before.split("\n")[:3]
                    )
                    after_lines = "".join(
                        f'<div class="diff-add">+ {line}</div>'
                        for line in snippet_after.split("\n")[:3]
                    )
                    diff_html = f'<div class="diff">{before_lines}{after_lines}</div>'
                samples_html += f'<p class="file-path" style="margin:4px 0">{_esc(sf.get("file_path","")[-60:])}</p>{diff_html}'

            status_badge = (
                '<span class="badge badge-yellow">skipped</span>' if skipped else ""
            )

            rows += f"""
<div class="card hint-card" data-search="{_esc(key.lower())}">
  <div class="card-header" onclick="this.nextElementSibling.classList.toggle('open')">
    <span>{_esc(key.split(" / ")[-1])} <span class="badge">{incident_count} incidents</span></span>
    {status_badge}
  </div>
  <div class="collapsible">
    {f'<p style="color:var(--yellow);margin:4px 0">Skipped: {_esc(h.get("skipped_reason",""))}</p>' if skipped else ''}
    {samples_html}
    <div class="hint-text">{_esc(h.get("hint_text",""))}</div>
  </div>
</div>"""

    return f"""
<div id="hints">
<h2>All Hints ({total})</h2>
<input class="search" type="text" placeholder="Filter by violation..." oninput="filterCards(this.value, 'hint-card')">
{rows}
</div>"""


def _footer() -> str:
    return """
<script>
function filterCards(query, className) {
  const q = query.toLowerCase();
  document.querySelectorAll('.' + className).forEach(card => {
    const text = card.getAttribute('data-search') || '';
    card.classList.toggle('hidden', q && !text.includes(q));
  });
}
function toggleLowRelevance(show) {
  document.querySelectorAll('.rule-card.low-relevance').forEach(card => {
    card.classList.toggle('hidden', !show);
  });
}
</script>
</body></html>"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m kai_commit_miner.report <output_dir> [report.html]",
            file=sys.stderr,
        )
        sys.exit(1)
    output_dir = Path(sys.argv[1])
    report_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    path = generate_html_report(output_dir, report_path)
    print(f"Report written to {path}")
