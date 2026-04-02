import hashlib
import json
from pathlib import Path

import yaml

from kai_mcp_solution_server.analyzer_types import AnalysisReport


class AnalysisCache:
    """File-based cache for analysis results, keyed by (commit_hash, config_hash)."""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, commit_hash: str, config_hash: str) -> str:
        return hashlib.sha256(f"{commit_hash}:{config_hash}".encode()).hexdigest()[:16]

    def _cache_path(self, commit_hash: str, config_hash: str) -> Path:
        key = self._cache_key(commit_hash, config_hash)
        return self.cache_dir / f"{key}.json"

    def get(self, commit_hash: str, config_hash: str) -> AnalysisReport | None:
        path = self._cache_path(commit_hash, config_hash)
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        if isinstance(data, list):
            return AnalysisReport(data)
        return None

    def put(self, commit_hash: str, config_hash: str, report: AnalysisReport) -> None:
        path = self._cache_path(commit_hash, config_hash)
        # Serialize rulesets to dicts
        data = [rs.model_dump(mode="json") for rs in report.root]
        path.write_text(json.dumps(data, indent=2))

    @staticmethod
    def compute_config_hash(config_path: Path | None) -> str:
        """Compute a hash of the analyzer config file for cache invalidation."""
        if config_path is None or not config_path.exists():
            return "no_config"
        content = config_path.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]
