"""Tests for commit walker and git repo wrapper."""

import subprocess
import tempfile
from pathlib import Path

from kai_commit_miner.git.commit_walker import LinearWalker, create_walker
from kai_commit_miner.git.repo import GitRepo


def _create_repo_with_commits(n: int = 4) -> tuple[Path, list[str]]:
    """Create a git repo with n commits, return path and commit hashes."""
    tmpdir = Path(tempfile.mkdtemp(prefix="kai_test_walker_"))
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
    # Use 'main' branch name
    subprocess.run(
        ["git", "checkout", "-b", "main"],
        cwd=tmpdir,
        capture_output=True,
        check=True,
    )

    hashes = []
    for i in range(n):
        (tmpdir / f"file{i}.txt").write_text(f"content {i}\n")
        subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"commit {i}"],
            cwd=tmpdir,
            capture_output=True,
            check=True,
        )
        h = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        hashes.append(h)

    return tmpdir, hashes


def test_linear_walker_yields_all_pairs() -> None:
    tmpdir, hashes = _create_repo_with_commits(4)
    repo = GitRepo(tmpdir)

    walker = LinearWalker()
    pairs = list(walker.walk(repo, branch="main"))

    assert len(pairs) == 3  # 4 commits -> 3 pairs
    assert pairs[0][0].hash == hashes[0]
    assert pairs[0][1].hash == hashes[1]
    assert pairs[2][0].hash == hashes[2]
    assert pairs[2][1].hash == hashes[3]


def test_linear_walker_with_start_end() -> None:
    tmpdir, hashes = _create_repo_with_commits(5)
    repo = GitRepo(tmpdir)

    walker = LinearWalker()
    pairs = list(walker.walk(repo, branch="main", start=hashes[1], end=hashes[3]))

    assert len(pairs) == 2
    assert pairs[0][0].hash == hashes[1]
    assert pairs[1][1].hash == hashes[3]


def test_create_walker_factory() -> None:
    walker = create_walker("linear")
    assert isinstance(walker, LinearWalker)


def test_git_repo_get_diff() -> None:
    tmpdir, hashes = _create_repo_with_commits(2)
    repo = GitRepo(tmpdir)
    diff = repo.get_diff(hashes[0], hashes[1])
    assert "file1.txt" in diff


def test_git_repo_get_file_at_commit() -> None:
    tmpdir, hashes = _create_repo_with_commits(2)
    repo = GitRepo(tmpdir)
    content = repo.get_file_at_commit(hashes[0], "file0.txt")
    assert "content 0" in content


def test_git_repo_get_changed_files() -> None:
    tmpdir, hashes = _create_repo_with_commits(2)
    repo = GitRepo(tmpdir)
    changed = repo.get_changed_files(hashes[0], hashes[1])
    assert "file1.txt" in changed


def test_git_repo_worktree() -> None:
    tmpdir, hashes = _create_repo_with_commits(2)
    repo = GitRepo(tmpdir)

    wt = repo.create_worktree(hashes[0])
    assert wt.exists()
    assert (wt / "file0.txt").exists()
    assert not (wt / "file1.txt").exists()  # file1 only in commit 1

    repo.remove_worktree(wt)
    assert not wt.exists()
