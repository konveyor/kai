# kai-commit-miner

Extract migration knowledge (hints and rules) from completed code migrations for the [KAI](https://github.com/konveyor/kai) project.

Given two git refs (before and after a migration), the miner:

1. **Infers the migration** from manifest diffs (pom.xml, package.json, etc.)
2. **Runs static analysis** on both refs via [kantra](https://github.com/konveyor/kantra) to find resolved violations
3. **Attributes fixes** to specific code changes in the diff
4. **Generates hints** per violation type — practical guidance that supplements the rule description
5. **Discovers new rules** from changes the analyzer missed, output as real [analyzer-lsp](https://github.com/konveyor/analyzer-lsp) YAML

## Quick start

```bash
cd kai_commit_miner
uv sync

# Mine a completed migration (dry-run, writes to local files)
uv run python -m kai_commit_miner \
  --repo-path /path/to/migrated-project \
  --start-commit <before-migration-ref> \
  --end-commit <after-migration-ref> \
  --dry-run \
  --llm-params-file llm-params.json

# Generate a markdown report
uv run python -m kai_commit_miner.report .kai_miner_output report.md
```

Where `llm-params.json` is:

```json
{ "model": "claude-sonnet-4-20250514", "model_provider": "anthropic" }
```

## How it works

```
start-commit ─────────────────────────────── end-commit
     │                                            │
     ├─ kantra analyze ──► analysis report (before)
     │                     analysis report (after) ◄── kantra analyze ─┤
     │                          │                                      │
     │                     diff reports                                │
     │                          │                                      │
     │                   204 resolved violations                       │
     │                          │                                      │
     └──── git diff ───────────►├── attribute to hunks                 │
                                │                                      │
                         ┌──────┴──────┐                               │
                   attributed     unattributed                         │
                   fixes          changes                              │
                      │               │                                │
                  LLM: hints     LLM: rules                            │
                      │               │                                │
                      └───────┬───────┘
                              │
                     hints.json + rule_candidates.json + report.md
```

## Analyzer backends

| Backend              | Flag                                                                 | Description                                                                                                                                        |
| -------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **kantra** (default) | `--analyzer-backend kantra`                                          | Runs kantra in container mode. Requires podman/docker. Auto-selects label selector from inferred migration.                                        |
| **precomputed**      | `--analyzer-backend precomputed --precomputed-reports-dir ./reports` | Loads pre-generated analysis YAML/JSON files keyed by commit hash.                                                                                 |
| **none**             | `--analyzer-backend none`                                            | Skips analysis entirely. Treats all code changes as unattributed — generates rules only, no hints. Useful for bootstrapping rulesets from scratch. |

## Output

Dry-run mode writes to `--dry-run-output-dir` (default `.kai_miner_output`):

| File                   | Description                                                         |
| ---------------------- | ------------------------------------------------------------------- |
| `hints.json`           | Hints per violation type with sample files and skip reasoning       |
| `rule_candidates.json` | Proposed analyzer-lsp rules with migration relevance and validation |
| `metadata.json`        | Migration description, labels, commit refs, stats                   |

Generate a report: `uv run python -m kai_commit_miner.report <output_dir> [report.md]`

## Examples

Sample reports from mining the [coolstore](https://github.com/konveyor-ecosystem/coolstore) Java EE 7 → Quarkus migration:

- **[With kantra analysis](examples/coolstore-javaee-to-quarkus.md)** — 204 violations resolved, 34 hints, 7 new rules ($0.67)
- **[Without analysis](examples/coolstore-no-analysis.md)** — diff-only mode, 15 rules discovered from scratch ($0.10)

## CLI reference

```
uv run python -m kai_commit_miner --help

Required:
  --repo-path PATH          Path to the git repository
  --start-commit REF        Before-migration ref (tag, branch, SHA)
  --end-commit REF          After-migration ref

Optional:
  --migration-description   Override auto-inference with explicit description
  --analyzer-backend        kantra | precomputed | none (default: kantra)
  --kantra-binary PATH      Path to kantra binary (default: kantra)
  --analyzer-config PATH    Custom kantra rules file
  --precomputed-reports-dir Path to pre-generated analysis reports
  --solution-server-url     URL for live mode (default: http://localhost:8000)
  --dry-run                 Write to local files instead of pushing to server
  --dry-run-output-dir      Output directory for dry-run (default: .kai_miner_output)
  --llm-params-file PATH    JSON file with langchain model config
  --cache-dir PATH          Cache directory for analysis results
```

## Development

```bash
uv sync
uv run pytest tests/                      # unit tests (32)
uv run pytest tests/ -k coolstore         # integration tests (require coolstore repo)
uv run mypy src/kai_commit_miner/
```
