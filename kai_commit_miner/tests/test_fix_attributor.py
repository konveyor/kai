"""Tests for fix attribution logic."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from kai_commit_miner.attribution.fix_attributor import attribute_fixes
from kai_commit_miner.diff.models import IncidentDelta, IncidentDeltaStatus
from kai_commit_miner.git.diff_parser import DiffHunk, FileDiff
from kai_commit_miner.git.repo import GitRepo
from kai_mcp_solution_server.analyzer_types import Category, ExtendedIncident
from kai_mcp_solution_server.db.python_objects import ViolationID


def _make_delta(
    uri: str = "src/Foo.java",
    line_number: int = 3,
    message: str = "javax import",
) -> IncidentDelta:
    return IncidentDelta(
        violation_key=ViolationID(
            ruleset_name="quarkus/springboot",
            violation_name="javax-to-jakarta",
        ),
        incident_before=ExtendedIncident(
            uri=uri,
            message=message,
            code_snip="import javax.ejb.Stateless;",
            line_number=line_number,
            variables={},
            ruleset_name="quarkus/springboot",
            ruleset_description="",
            violation_name="javax-to-jakarta",
            violation_description="",
            violation_category=Category.MANDATORY,
            violation_labels=[],
        ),
        status=IncidentDeltaStatus.RESOLVED,
    )


def _make_file_diff(
    path: str = "src/Foo.java",
    old_start: int = 1,
    old_count: int = 5,
) -> FileDiff:
    return FileDiff(
        old_path=path,
        new_path=path,
        hunks=[
            DiffHunk(
                old_start=old_start,
                old_count=old_count,
                new_start=old_start,
                new_count=old_count,
                content="@@ hunk content @@\n-old\n+new",
                removed_lines=[old_start + 1],
                added_lines=[old_start + 1],
            )
        ],
    )


def _create_test_repo() -> tuple[GitRepo, str, str]:
    """Create a small git repo with 2 commits for testing."""
    tmpdir = Path(tempfile.mkdtemp(prefix="kai_test_repo_"))
    subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmpdir,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmpdir,
        capture_output=True,
        check=True,
    )

    # Commit 1: before state
    src = tmpdir / "src"
    src.mkdir()
    (src / "Foo.java").write_text(
        "package com.example;\nimport javax.ejb.Stateless;\n@Stateless\npublic class Foo {}\n"
    )
    subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=tmpdir,
        capture_output=True,
        check=True,
    )
    c1 = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmpdir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    # Commit 2: after state (javax -> jakarta)
    (src / "Foo.java").write_text(
        "package com.example;\nimport jakarta.ejb.Stateless;\n@Stateless\npublic class Foo {}\n"
    )
    subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "migrate javax to jakarta"],
        cwd=tmpdir,
        capture_output=True,
        check=True,
    )
    c2 = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmpdir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    return GitRepo(tmpdir), c1, c2


def test_attribute_fix_with_overlap() -> None:
    """Incident at line 3 overlaps with hunk at lines 1-5."""
    repo, c1, c2 = _create_test_repo()

    delta = _make_delta(uri="src/Foo.java", line_number=2)
    file_diff = _make_file_diff(path="src/Foo.java", old_start=1, old_count=5)

    attributed, unattributed = attribute_fixes([delta], [file_diff], repo, c1, c2)

    assert len(attributed) == 1
    assert attributed[0].indirect is False
    assert len(attributed[0].relevant_hunks) == 1
    assert "javax" in attributed[0].before_content
    assert "jakarta" in attributed[0].after_content


def test_attribute_fix_no_overlap_marked_indirect() -> None:
    """Incident at line 100 doesn't overlap with hunk at lines 1-5."""
    repo, c1, c2 = _create_test_repo()

    delta = _make_delta(uri="src/Foo.java", line_number=100)
    file_diff = _make_file_diff(path="src/Foo.java", old_start=1, old_count=3)

    attributed, unattributed = attribute_fixes([delta], [file_diff], repo, c1, c2)

    assert len(attributed) == 1
    assert attributed[0].indirect is True
    assert len(attributed[0].relevant_hunks) == 0


def test_attribute_fix_no_diff_for_file() -> None:
    """Incident in a file that has no diff -> indirect resolution."""
    repo, c1, c2 = _create_test_repo()

    delta = _make_delta(uri="src/Other.java", line_number=5)

    attributed, unattributed = attribute_fixes([delta], [], repo, c1, c2)

    assert len(attributed) == 1
    assert attributed[0].indirect is True


def test_unattributed_changes_collected() -> None:
    """Hunks not claimed by any incident go to unattributed."""
    repo, c1, c2 = _create_test_repo()

    # No resolved incidents
    file_diff = _make_file_diff(path="src/Foo.java")

    attributed, unattributed = attribute_fixes([], [file_diff], repo, c1, c2)

    assert len(attributed) == 0
    assert len(unattributed) == 1
    assert unattributed[0].file_path == "src/Foo.java"
