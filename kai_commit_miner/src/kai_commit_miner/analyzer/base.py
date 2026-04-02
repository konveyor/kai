from pathlib import Path
from typing import Protocol, runtime_checkable

from kai_commit_miner.config import MinerSettings
from kai_mcp_solution_server.analyzer_types import AnalysisReport


@runtime_checkable
class AnalyzerBackend(Protocol):
    """Protocol for pluggable analysis backends."""

    async def analyze(
        self,
        repo_path: Path,
        config: MinerSettings,
        commit_hash: str = "",
    ) -> AnalysisReport:
        """Run analysis on the repo checkout and return a report."""
        ...
