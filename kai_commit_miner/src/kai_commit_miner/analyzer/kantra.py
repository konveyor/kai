import asyncio
import sys
import tempfile
from pathlib import Path

from kai_commit_miner.analyzer.precomputed import load_report
from kai_commit_miner.config import MinerSettings
from kai_mcp_solution_server.analyzer_types import AnalysisReport


class KantraBackend:
    """Analyzer backend that shells out to the kantra CLI.

    Uses container mode by default (--run-local=false) which requires
    podman or docker to be running. Container mode bundles all Java
    tooling so no local jdtls installation is needed.
    """

    async def analyze(
        self,
        repo_path: Path,
        config: MinerSettings,
        commit_hash: str = "",
    ) -> AnalysisReport:
        output_dir = tempfile.mkdtemp(prefix="kai_kantra_out_")
        output_subdir = str(Path(output_dir) / "results")

        cmd = [
            config.kantra_binary,
            "analyze",
            "--input",
            str(repo_path.resolve()),
            "--output",
            output_subdir,
            "--mode",
            "source-only",
            "--no-progress",
            "--run-local=false",
        ]

        if config.analyzer_config_path is not None:
            cmd.extend(["--rules", str(config.analyzer_config_path.resolve())])

        if config.analyzer_label_selector:
            cmd.extend(["--label-selector", config.analyzer_label_selector])

        print(f"    kantra: {commit_hash[:8]} ...", file=sys.stderr, flush=True)

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            err_text = stderr.decode()[-500:]
            raise RuntimeError(
                f"kantra analyze failed for {commit_hash[:8]} (exit {proc.returncode}):\n{err_text}"
            )

        output_path = Path(output_subdir)
        for candidate in ["output.yaml", "output.json"]:
            result_file = output_path / candidate
            if result_file.exists():
                return load_report(result_file)

        raise FileNotFoundError(
            f"No analysis output for {commit_hash[:8]} in {output_subdir}"
        )
