import argparse
import asyncio
import json
import sys
from pathlib import Path

from kai_commit_miner.config import MinerSettings
from kai_commit_miner.pipeline import MiningPipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mine migration knowledge from a completed migration"
    )
    parser.add_argument(
        "--repo-path", type=Path, required=True, help="Path to the git repository"
    )
    parser.add_argument(
        "--start-commit",
        type=str,
        required=True,
        help="Before-migration ref (tag, branch, SHA)",
    )
    parser.add_argument(
        "--end-commit",
        type=str,
        required=True,
        help="After-migration ref (tag, branch, SHA)",
    )
    parser.add_argument(
        "--migration-description",
        type=str,
        default=None,
        help="Migration description (inferred from manifests if omitted)",
    )
    parser.add_argument(
        "--analyzer-backend",
        choices=["kantra", "precomputed", "none"],
        default="kantra",
    )
    parser.add_argument("--kantra-binary", type=str, default="kantra")
    parser.add_argument("--analyzer-config", type=Path, default=None)
    parser.add_argument("--precomputed-reports-dir", type=Path, default=None)
    parser.add_argument(
        "--solution-server-url", type=str, default="http://localhost:8000"
    )
    parser.add_argument("--client-id", type=str, default="kai_commit_miner")
    parser.add_argument("--cache-dir", type=Path, default=Path(".kai_miner_cache"))
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write results to local files instead of pushing to server",
    )
    parser.add_argument(
        "--dry-run-output-dir", type=Path, default=Path(".kai_miner_output")
    )
    parser.add_argument("--llm-params-file", type=Path, default=None)

    args = parser.parse_args()

    llm_params = None
    if args.llm_params_file is not None:
        with open(args.llm_params_file) as f:
            llm_params = json.load(f)

    settings = MinerSettings(
        repo_path=args.repo_path,
        start_commit=args.start_commit,
        end_commit=args.end_commit,
        migration_description=args.migration_description,
        analyzer_backend=args.analyzer_backend,
        kantra_binary=args.kantra_binary,
        analyzer_config_path=args.analyzer_config,
        precomputed_reports_dir=args.precomputed_reports_dir,
        solution_server_url=args.solution_server_url,
        solution_server_client_id=args.client_id,
        cache_dir=args.cache_dir,
        dry_run=args.dry_run,
        dry_run_output_dir=args.dry_run_output_dir,
        llm_params=llm_params,
    )

    pipeline = MiningPipeline(settings)
    report = asyncio.run(pipeline.run())

    print(f"\nMining complete.", file=sys.stderr)
    print(f"  Violations resolved: {report.violations_resolved}", file=sys.stderr)
    print(f"  Hints generated: {report.hints_generated}", file=sys.stderr)
    print(f"  Rule candidates: {report.rule_candidates_found}", file=sys.stderr)
    if report.errors:
        print(f"  Errors: {len(report.errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
