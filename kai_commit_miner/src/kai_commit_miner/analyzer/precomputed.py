import json
from pathlib import Path

import yaml

from kai_commit_miner.config import MinerSettings
from kai_mcp_solution_server.analyzer_types import AnalysisReport


class PrecomputedBackend:
    """Analyzer backend that loads pre-computed reports from files.

    Looks for reports in the precomputed_reports_dir keyed by commit hash.
    Supports both YAML and JSON formats.
    """

    async def analyze(
        self,
        repo_path: Path,
        config: MinerSettings,
        commit_hash: str = "",
    ) -> AnalysisReport:
        if config.precomputed_reports_dir is None:
            raise ValueError(
                "precomputed_reports_dir must be set for PrecomputedBackend"
            )

        reports_dir = config.precomputed_reports_dir

        for pattern in [
            f"{commit_hash}*.yaml",
            f"{commit_hash}*.json",
            f"{commit_hash}*.yml",
        ]:
            matches = list(reports_dir.glob(pattern))
            if matches:
                return load_report(matches[0])

        raise FileNotFoundError(
            f"No precomputed report found for commit {commit_hash} in {reports_dir}"
        )


def load_report(path: Path) -> AnalysisReport:
    """Load an AnalysisReport from a YAML or JSON file."""
    content = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        data = yaml.safe_load(content)
    else:
        data = json.loads(content)

    if isinstance(data, list):
        return AnalysisReport(data)
    raise ValueError(f"Expected list of rulesets, got {type(data)}")
