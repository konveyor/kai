from abc import ABC, abstractmethod
from collections.abc import Iterator

from kai_commit_miner.git.repo import CommitInfo, GitRepo


class CommitWalker(ABC):
    """Abstract base class for commit walking strategies."""

    @abstractmethod
    def walk(
        self,
        repo: GitRepo,
        branch: str,
        start: str | None = None,
        end: str | None = None,
    ) -> Iterator[tuple[CommitInfo, CommitInfo]]:
        """Yield adjacent commit pairs (before, after) to analyze."""
        ...


class LinearWalker(CommitWalker):
    """Walk all commits in linear order on the specified branch."""

    def walk(
        self,
        repo: GitRepo,
        branch: str,
        start: str | None = None,
        end: str | None = None,
    ) -> Iterator[tuple[CommitInfo, CommitInfo]]:
        commits = repo.get_commit_list(branch=branch, start=start, end=end)
        for i in range(len(commits) - 1):
            yield commits[i], commits[i + 1]


def create_walker(strategy: str) -> CommitWalker:
    """Factory for creating commit walkers by strategy name."""
    walkers: dict[str, type[CommitWalker]] = {
        "linear": LinearWalker,
    }
    if strategy not in walkers:
        raise ValueError(
            f"Unknown commit strategy: {strategy}. Available: {list(walkers.keys())}"
        )
    return walkers[strategy]()
