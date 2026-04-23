import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CommitInfo:
    hash: str
    author: str
    date: str
    message: str
    parent_hashes: list[str] = field(default_factory=list)


class GitRepo:
    """Wraps git CLI operations on a local repository."""

    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path.resolve()
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"{repo_path} is not a git repository")

    def _run(self, *args: str, cwd: Path | None = None) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def get_commit_list(
        self,
        branch: str = "main",
        start: str | None = None,
        end: str | None = None,
    ) -> list[CommitInfo]:
        """Get commits in topological order (oldest first)."""
        rev_range = branch
        if start and end:
            rev_range = f"{start}^..{end}"
        elif start:
            rev_range = f"{start}^..{branch}"
        elif end:
            rev_range = end

        # Format: hash|author|date|parents|subject
        log_output = self._run(
            "log",
            "--reverse",
            "--format=%H|%an|%aI|%P|%s",
            rev_range,
        )

        commits: list[CommitInfo] = []
        for line in log_output.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 4)
            if len(parts) < 5:
                continue
            commits.append(
                CommitInfo(
                    hash=parts[0],
                    author=parts[1],
                    date=parts[2],
                    parent_hashes=parts[3].split() if parts[3] else [],
                    message=parts[4],
                )
            )
        return commits

    def get_diff(self, commit_a: str, commit_b: str) -> str:
        """Get unified diff between two commits."""
        return self._run("diff", commit_a, commit_b)

    def get_file_at_commit(self, commit_hash: str, file_path: str) -> str:
        """Read a file's content at a specific commit."""
        return self._run("show", f"{commit_hash}:{file_path}")

    def get_changed_files(self, commit_a: str, commit_b: str) -> list[str]:
        """Get list of files changed between two commits."""
        output = self._run("diff", "--name-only", commit_a, commit_b)
        return [f for f in output.strip().split("\n") if f]

    def create_worktree(self, commit_hash: str) -> Path:
        """Create a temporary git worktree checked out at the given commit."""
        worktree_dir = Path(tempfile.mkdtemp(prefix=f"kai_miner_{commit_hash[:8]}_"))
        self._run("worktree", "add", "--detach", str(worktree_dir), commit_hash)
        return worktree_dir

    def remove_worktree(self, worktree_path: Path) -> None:
        """Remove a git worktree."""
        self._run("worktree", "remove", "--force", str(worktree_path))

    def merge_base(self, commit: str, branch: str) -> str | None:
        """Find the merge base between a commit and a branch."""
        try:
            return self._run("merge-base", commit, branch).strip() or None
        except Exception:
            return None

    def diff_files(self, commit_a: str, commit_b: str, *paths: str) -> str:
        """Get diff between two commits, optionally filtered to specific file paths."""
        args = ["diff", commit_a, commit_b]
        if paths:
            args.append("--")
            args.extend(paths)
        return self._run(*args)

    def diff_stat(self, commit_a: str, commit_b: str) -> str:
        """Get diff stat summary between two commits."""
        return self._run("diff", "--stat", commit_a, commit_b)
