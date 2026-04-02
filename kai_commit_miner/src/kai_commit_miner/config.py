from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class AnalyzerBackendType(StrEnum):
    KANTRA = "kantra"
    PRECOMPUTED = "precomputed"
    NONE = "none"  # Skip analysis, treat all diffs as unattributed


class MinerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_miner_")

    # Required inputs
    repo_path: Path
    start_commit: str  # Before-migration ref (tag, branch, SHA)
    end_commit: str  # After-migration ref

    # Optional
    migration_description: str | None = (
        None  # Inferred from manifest diffs if not provided
    )

    # Analyzer config
    analyzer_backend: AnalyzerBackendType = AnalyzerBackendType.KANTRA
    kantra_binary: str = "kantra"
    analyzer_config_path: Path | None = None
    analyzer_label_selector: str | None = (
        None  # Set automatically from migration inference
    )
    precomputed_reports_dir: Path | None = None

    # Solution server
    solution_server_url: str = "http://localhost:8000"
    solution_server_client_id: str = "kai_commit_miner"

    # LLM config (same format as solution server)
    llm_params: dict[str, Any] | None = None

    # Performance
    cache_dir: Path = Path(".kai_miner_cache")

    # Dry run mode
    dry_run: bool = False
    dry_run_output_dir: Path = Path(".kai_miner_output")
