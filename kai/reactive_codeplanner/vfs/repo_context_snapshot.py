import functools
import subprocess  # trunk-ignore(bandit/B404)
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from kai.constants import ENV
from kai.logging.logging import TRACE, get_logger

log = get_logger(__name__)


# NOTE: I'd like to use GitPython, but using custom a work-tree and git-dir with
# it is too hard.
@dataclass(frozen=True)
class RepoContextSnapshot:
    work_tree: Path  # project root
    snapshot_work_dir: Path  # .kai directory where all the repos live
    git_dir: Path
    git_sha: str

    parent: Optional["RepoContextSnapshot"] = None
    children: list["RepoContextSnapshot"] = field(default_factory=list)

    @functools.cached_property
    def msg(self) -> str:
        """
        msg is derived from the commit message of the git_sha. Use
        cached_property to maintain semblance of immutability.
        """
        returncode, stdout, stderr = self.git(
            ["show", "-s", "--format=%B", self.git_sha]
        )
        if returncode != 0:
            raise Exception(f"Failed to get commit message: {stderr}")

        return stdout.strip()

    @functools.cached_property
    def lineage(self) -> list["RepoContextSnapshot"]:
        """
        Returns the lineage of the current snapshot, starting from the initial
        commit. In order from oldest to newest.
        """
        lineage: list[RepoContextSnapshot] = [self]
        parent = self.parent
        while parent is not None:
            lineage.append(parent)
            parent = parent.parent

        lineage.reverse()

        return lineage

    def git(
        self, args: list[str], popen_kwargs: dict[str, Any] | None = None
    ) -> tuple[int | Any, str, str]:
        """
        Execute a git command with the given arguments. Returns a tuple of the
        return code, stdout, and stderr.
        """
        if popen_kwargs is None:
            popen_kwargs = {}

        GIT = [
            "git",
            "--git-dir",
            str(self.git_dir),
            "--work-tree",
            str(self.work_tree),
        ]
        popen_kwargs = {
            "cwd": self.work_tree,
            "env": ENV,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            **popen_kwargs,
        }

        log.log(TRACE, "executing: " + " ".join(GIT + args))
        proc = subprocess.Popen(GIT + args, **popen_kwargs)  # trunk-ignore(bandit/B603)
        stdout, stderr = proc.communicate()

        log.log(TRACE, f"returncode: {proc.returncode}")
        log.log(TRACE, f"stdout:\n{stdout}")
        log.log(TRACE, f"stderr:\n{stderr}")

        return proc.returncode, stdout, stderr

    @staticmethod
    def initialize(
        git_work_tree: Path, snapshot_work_dir: Path, msg: str | None = None
    ) -> "RepoContextSnapshot":
        """
        Creates a new git repo in the given work_tree, and returns a
        GitVFSSnapshot.
        """
        if msg is None:
            msg = "Initial commit"

        git_work_tree = git_work_tree.resolve()
        snapshot_work_dir.mkdir(exist_ok=True)
        # fmt: off
        # Note that windows can not use : characters in the filename/path, Black doesn't like this syntax on 3.11
        git_dir_suffix = datetime.now(timezone.utc).strftime("%Y-%m-%d-_%H-%M-%S")
        git_dir = snapshot_work_dir / f".git-{git_dir_suffix}"
        # fmt: on
        git_dir.mkdir(exist_ok=True)

        # Snapshot is immutable, so we create a temporary snapshot to get the
        # git sha of the initial commit
        tmp_snapshot = RepoContextSnapshot(
            work_tree=git_work_tree,
            snapshot_work_dir=snapshot_work_dir,
            git_dir=git_dir,
            git_sha="",
        )

        returncode, _, stderr = tmp_snapshot.git(["init"])
        if returncode != 0:
            raise Exception(f"Failed to initialize git repository: {stderr}")

        with open(git_dir / "info" / "exclude", "a") as f:
            f.write(f"/{str(snapshot_work_dir.name)}\n")

        returncode, _, stderr = tmp_snapshot.git(["config", "commit.gpgsign", "false"])
        if returncode != 0:
            raise Exception(f"Failed to disable gpgsign: {stderr}")

        returncode, _, stderr = tmp_snapshot.git(
            ["config", "user.email", "kai-agent@example.com"]
        )
        if returncode != 0:
            raise Exception(f"Failed to set user.email: {stderr}")
        returncode, _, stderr = tmp_snapshot.git(["config", "user.name", "KaiAgent"])
        if returncode != 0:
            raise Exception(f"Failed to set user.name: {stderr}")

        tmp_snapshot = tmp_snapshot.commit(msg)

        return RepoContextSnapshot(
            work_tree=git_work_tree,
            snapshot_work_dir=snapshot_work_dir,
            git_dir=git_dir,
            git_sha=tmp_snapshot.git_sha,
            parent=None,
            children=[],
        )

    def commit(
        self,
        msg: str | None = None,
    ) -> "RepoContextSnapshot":
        """
        Commits the current state of the repository and returns a new snapshot.
        Automatically sets the commit message to the current time if none is
        provided. The children and parent fields are updated accordingly.
        """
        if msg is None:
            msg = f"Auto-generated commit message ({datetime.now(timezone.utc).isoformat()})"

        returncode, stdout, stderr = self.git(["add", "."])
        if returncode != 0:
            raise Exception(f"Failed to add files to git repository: {stderr}")

        returncode, _, stderr = self.git(
            ["commit", "--allow-empty", "--allow-empty-message", "-m", msg]
        )
        if returncode != 0:
            raise Exception(f"Failed to create commit: {stderr}")

        returncode, stdout, stderr = self.git(["rev-parse", "HEAD"])
        if returncode != 0:
            raise Exception(f"Failed to get HEAD: {stderr}")

        result = RepoContextSnapshot(
            work_tree=self.work_tree,
            snapshot_work_dir=self.snapshot_work_dir,
            git_dir=self.git_dir,
            git_sha=stdout.strip(),
            parent=self,
        )

        self.children.append(result)

        return result

    def reset(self) -> tuple[int, str, str]:
        """
        Reset the state of the repository to the current snapshot.
        """
        return self.git(["reset", "--hard", self.git_sha])

    def diff(self, other: "RepoContextSnapshot") -> tuple[int, str, str]:
        """
        Returns the diff between the current snapshot and another snapshot.
        """
        result = self.git(["diff", other.git_sha, self.git_sha])
        if not result[1].endswith("\n"):  # HACK: This may not be needed
            result = result[0], result[1] + "\n", result[2]

        return result
