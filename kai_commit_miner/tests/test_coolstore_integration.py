"""Integration tests using the coolstore repo.

These tests require:
- The coolstore repo cloned at /Users/fabian/projects/github.com/konveyor/coolstore
- For kantra tests: kantra binary in PATH or ~/bin/kantra
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from kai_commit_miner.analyzer.cache import AnalysisCache
from kai_commit_miner.attribution.fix_attributor import attribute_fixes
from kai_commit_miner.config import AnalyzerBackendType, MinerSettings
from kai_commit_miner.diff.models import IncidentDeltaStatus
from kai_commit_miner.diff.report_differ import diff_reports
from kai_commit_miner.git.diff_parser import parse_unified_diff
from kai_commit_miner.git.repo import GitRepo
from kai_commit_miner.pipeline import MiningPipeline
from kai_mcp_solution_server.analyzer_types import AnalysisReport

COOLSTORE_PATH = Path("/Users/fabian/projects/github.com/konveyor/coolstore")
KAI_ANALYSIS_PATH = Path(
    "/Users/fabian/projects/github.com/konveyor/kai/example/analysis/coolstore/output.yaml"
)

# First 3 migration commits on the quarkus branch (full hashes for precomputed backend)
COMMIT_MAIN = "b5752b9"  # last commit on main (short, used for git ops)
COMMIT_POM = "b4fee3a"  # Migrate POM to Quarkus deps
COMMIT_POM_FULL = "b4fee3a0aef169e9da0792e48947e78c431bdd43"
COMMIT_IMPORTS = "b49496d"  # javax -> jakarta imports
COMMIT_IMPORTS_FULL = "b49496d66fd190bdc694dd641c08365f77047ea5"
COMMIT_JMS = "15bde8c"  # JMS/MDB to SmallRye


def _coolstore_available() -> bool:
    return COOLSTORE_PATH.exists() and (COOLSTORE_PATH / ".git").exists()


def _kantra_available() -> bool:
    for path in [Path.home() / "bin" / "kantra", Path("/usr/local/bin/kantra")]:
        if path.exists():
            return True
    # Also check PATH
    result = subprocess.run(["which", "kantra"], capture_output=True)
    return result.returncode == 0


def _load_analysis_output() -> AnalysisReport:
    """Load the existing coolstore analysis output (analysis of main branch)."""
    with open(KAI_ANALYSIS_PATH) as f:
        data = yaml.safe_load(f)
    return AnalysisReport(data)


@unittest.skipUnless(_coolstore_available(), "coolstore repo not available")
class TestCoolstoreReportDiffing(unittest.TestCase):
    """Test report diffing with real coolstore analysis data."""

    def test_diff_main_vs_empty_shows_all_resolved(self) -> None:
        """When all violations are resolved, diff should show them all as resolved."""
        main_report = _load_analysis_output()
        empty_report = AnalysisReport([])

        result = diff_reports(main_report, empty_report, "main", "quarkus")

        self.assertGreater(len(result.resolved), 0)
        self.assertEqual(len(result.new), 0)
        self.assertEqual(len(result.unchanged), 0)

        # Check we got real violations
        violation_names = {d.violation_key.violation_name for d in result.resolved}
        # The coolstore analysis should have javax-related violations
        self.assertGreater(len(violation_names), 0)

    def test_diff_same_report_shows_no_changes(self) -> None:
        main_report = _load_analysis_output()
        result = diff_reports(main_report, main_report, "main", "main")

        self.assertEqual(len(result.resolved), 0)
        self.assertEqual(len(result.new), 0)
        self.assertGreater(len(result.unchanged), 0)


@unittest.skipUnless(_coolstore_available(), "coolstore repo not available")
class TestCoolstoreGitOperations(unittest.TestCase):
    """Test git operations on the real coolstore repo."""

    def test_get_commit_list(self) -> None:
        repo = GitRepo(COOLSTORE_PATH)
        commits = repo.get_commit_list(
            branch="origin/quarkus",
            start=COMMIT_POM,
            end=COMMIT_JMS,
        )
        self.assertEqual(len(commits), 3)
        self.assertIn("POM", commits[0].message)
        self.assertIn("import", commits[1].message)
        self.assertIn("JMS", commits[2].message)

    def test_get_diff_import_migration(self) -> None:
        repo = GitRepo(COOLSTORE_PATH)
        diff = repo.get_diff(COMMIT_POM, COMMIT_IMPORTS)
        # The import migration commit should change javax -> jakarta
        self.assertIn("javax", diff)
        self.assertIn("jakarta", diff)

    def test_get_changed_files(self) -> None:
        repo = GitRepo(COOLSTORE_PATH)
        changed = repo.get_changed_files(COMMIT_POM, COMMIT_IMPORTS)
        # The import commit changes .java files
        java_files = [f for f in changed if f.endswith(".java")]
        self.assertGreater(len(java_files), 0)

    def test_get_file_at_commit(self) -> None:
        repo = GitRepo(COOLSTORE_PATH)
        # Before import migration, files should have javax
        content = repo.get_file_at_commit(
            COMMIT_POM,
            "src/main/java/com/redhat/coolstore/model/Order.java",
        )
        self.assertIn("javax", content)

        # After import migration, files should have jakarta
        content = repo.get_file_at_commit(
            COMMIT_IMPORTS,
            "src/main/java/com/redhat/coolstore/model/Order.java",
        )
        self.assertIn("jakarta", content)


@unittest.skipUnless(_coolstore_available(), "coolstore repo not available")
class TestCoolstoreFixAttribution(unittest.TestCase):
    """Test fix attribution with real coolstore diffs."""

    def test_attribute_import_migration_fixes(self) -> None:
        """The import migration commit should attribute javax->jakarta incidents."""
        repo = GitRepo(COOLSTORE_PATH)

        # Load main analysis and create an empty one for "after"
        main_report = _load_analysis_output()
        empty_report = AnalysisReport([])

        report_diff = diff_reports(
            main_report, empty_report, COMMIT_POM, COMMIT_IMPORTS
        )

        # Filter to just resolved incidents in java files
        java_resolved = [
            d
            for d in report_diff.resolved
            if d.incident_before and d.incident_before.uri.endswith(".java")
        ]
        self.assertGreater(len(java_resolved), 0)

        # Get the real git diff
        git_diff = repo.get_diff(COMMIT_POM, COMMIT_IMPORTS)
        file_diffs = parse_unified_diff(git_diff)

        attributed, unattributed = attribute_fixes(
            java_resolved[:10],  # Limit to first 10 for speed
            file_diffs,
            repo,
            COMMIT_POM,
            COMMIT_IMPORTS,
        )

        # Some should be directly attributed (file path + line overlap)
        self.assertGreater(len(attributed), 0)

        # Check that attributed fixes have content
        for fix in attributed:
            if not fix.indirect:
                self.assertGreater(len(fix.relevant_hunks), 0)


@unittest.skipUnless(
    _coolstore_available() and _kantra_available(),
    "coolstore repo and kantra not available",
)
class TestCoolstoreKantraAnalysis(unittest.IsolatedAsyncioTestCase):
    """Test running kantra on the coolstore repo.

    These tests are slow (kantra analysis takes 30-60s per run).
    Run with: pytest -k kantra -v
    """

    async def test_kantra_analyze_main_branch(self) -> None:
        """Run kantra on the main branch and verify we get violations."""
        from kai_commit_miner.analyzer.kantra import KantraBackend

        kantra_bin = str(Path.home() / "bin" / "kantra")
        if not Path(kantra_bin).exists():
            kantra_bin = "kantra"

        settings = MinerSettings(
            repo_path=COOLSTORE_PATH,
            migration_description="Java EE to Quarkus",
            kantra_binary=kantra_bin,
            solution_server_url="http://localhost:8000",
        )

        backend = KantraBackend()
        repo = GitRepo(COOLSTORE_PATH)
        worktree = repo.create_worktree(COMMIT_MAIN)

        try:
            report = await backend.analyze(worktree, settings, COMMIT_MAIN)
            # Should find some rulesets with violations
            total_incidents = sum(
                len(v.incidents or [])
                for rs in report.root
                for v in (rs.violations or {}).values()
            )
            self.assertGreater(total_incidents, 0)
        finally:
            repo.remove_worktree(worktree)


@unittest.skipUnless(_coolstore_available(), "coolstore repo not available")
class TestCoolstorePipelineDryRun(unittest.IsolatedAsyncioTestCase):
    """Test the full pipeline in dry-run mode with precomputed reports."""

    async def test_pipeline_dry_run_with_precomputed(self) -> None:
        """Run the pipeline in dry-run mode using the existing analysis output.

        We'll create precomputed reports:
        - main commit -> the existing analysis output (has violations)
        - first migration commit -> empty report (all violations resolved)
        """
        with tempfile.TemporaryDirectory(prefix="kai_test_pipeline_") as tmpdir:
            reports_dir = Path(tmpdir) / "reports"
            reports_dir.mkdir()
            output_dir = Path(tmpdir) / "output"

            # Use the existing analysis output as the "before" report (POM commit)
            # and an empty report as the "after" (imports commit, all resolved)
            main_report = _load_analysis_output()
            with open(reports_dir / f"{COMMIT_POM_FULL}.yaml", "w") as f:
                yaml.dump(
                    [rs.model_dump(mode="json") for rs in main_report.root],
                    f,
                )

            # Create an empty report for the "after" state (all resolved)
            with open(reports_dir / f"{COMMIT_IMPORTS_FULL}.yaml", "w") as f:
                yaml.dump([], f)

            settings = MinerSettings(
                repo_path=COOLSTORE_PATH,
                migration_description="Java EE 7 to Quarkus 3.x",
                analyzer_backend=AnalyzerBackendType.PRECOMPUTED,
                precomputed_reports_dir=reports_dir,
                start_commit=COMMIT_POM,
                end_commit=COMMIT_IMPORTS,
                solution_server_url="http://localhost:8000",
                llm_params={
                    "model": "fake",
                    "responses": [
                        "SUMMARY:\nMigrate POM deps\n\nHINT:\n1. Update pom.xml",
                        "[]",
                    ],
                },
                dry_run=True,
                dry_run_output_dir=output_dir,
                cache_dir=Path(tmpdir) / "cache",
            )

            pipeline = MiningPipeline(settings)
            report = await pipeline.run()

            self.assertGreater(report.violations_resolved, 0)
            self.assertGreater(report.hints_generated, 0)

            # Verify dry-run output files were created
            self.assertTrue((output_dir / "hints.json").exists())
            self.assertTrue((output_dir / "rule_candidates.json").exists())

            hints = json.loads((output_dir / "hints.json").read_text())
            self.assertGreater(len(hints), 0)
