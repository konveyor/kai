import argparse
import functools
import logging
import os
import subprocess  # trunk-ignore(bandit/B404)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Optional

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import AgentResult
from kai.reactive_codeplanner.agent.reflection_agent import (
    ReflectionAgent,
    ReflectionTask,
)

log = get_logger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)


class SpawningResult(ABC):
    @abstractmethod
    def to_reflection_task(self) -> Optional[ReflectionTask]:
        pass


# NOTE: I'd like to use GitPython, but using custom a work-tree and git-dir with
# it is too hard.
@dataclass(frozen=True)
class RepoContextSnapshot:
    work_tree: Path  # project root
    git_dir: Path
    git_sha: str

    parent: Optional["RepoContextSnapshot"] = None
    children: list["RepoContextSnapshot"] = field(default_factory=list)

    spawning_result: Optional[SpawningResult] = None

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
    def parent_spawning_results(self) -> list[SpawningResult]:
        """
        Returns a list of spawning results from the parent snapshots, including
        itself, in order from oldest to newest.
        """

        if not self.spawning_result:
            return []

        if self.parent is None:
            return [self.spawning_result]

        return self.parent.parent_spawning_results + [self.spawning_result]

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
            "env": dict(os.environ),
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            **popen_kwargs,
        }

        log.debug("\033[94mexecuting: \033[0m" + " ".join(GIT + args))
        proc = subprocess.Popen(GIT + args, **popen_kwargs)  # trunk-ignore(bandit/B603)
        stdout, stderr = proc.communicate()

        log.debug(f"\033[94mreturncode:\033[0m {proc.returncode}")
        log.debug(f"\033[94mstdout:\033[0m\n{stdout}")
        log.debug(f"\033[94mstderr:\033[0m\n{stderr}")

        return proc.returncode, stdout, stderr

    @staticmethod
    def initialize(work_tree: Path, msg: str | None = None) -> "RepoContextSnapshot":
        """
        Creates a new git repo in the given work_tree, and returns a
        GitVFSSnapshot.
        """
        if msg is None:
            msg = "Initial commit"

        work_tree = work_tree.resolve()
        kai_dir = work_tree / ".kai"
        kai_dir.mkdir(exist_ok=True)
        git_dir = kai_dir / f".git-{datetime.now(timezone.utc).isoformat()}"

        # Snapshot is immutable, so we create a temporary snapshot to get the
        # git sha of the initial commit
        tmp_snapshot = RepoContextSnapshot(
            work_tree=work_tree,
            git_dir=git_dir,
            git_sha="",
        )

        returncode, _, stderr = tmp_snapshot.git(["init"])
        if returncode != 0:
            raise Exception(f"Failed to initialize git repository: {stderr}")

        with open(git_dir / "info" / "exclude", "a") as f:
            f.write(f"/{str(kai_dir.name)}\n")

        tmp_snapshot = tmp_snapshot.commit(msg)

        return RepoContextSnapshot(
            work_tree=work_tree,
            git_dir=git_dir,
            git_sha=tmp_snapshot.git_sha,
            parent=None,
            children=[],
        )

    def commit(
        self, msg: str | None = None, spawning_result: SpawningResult | None = None
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
            git_dir=self.git_dir,
            git_sha=stdout.strip(),
            parent=self,
            spawning_result=spawning_result,
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
        return self.git(["diff", other.git_sha, self.git_sha])


class RepoContextManager:
    def __init__(
        self,
        project_root: Path,
        reflection_agent: Optional[ReflectionAgent] = None,
        initial_msg: str | None = None,
    ):
        self.project_root = project_root
        self.snapshot = RepoContextSnapshot.initialize(project_root, initial_msg)
        self.first_snapshot = self.snapshot
        self.reflection_agent = reflection_agent

    def commit(
        self, msg: str | None = None, spawning_result: SpawningResult | None = None
    ) -> bool:
        """
        Commits the current state of the repository and updates the snapshot.
        Also runs the reflection agent validate the repository state.
        """

        reflection_result = AgentResult(encountered_errors=[], modified_files=None)
        if self.reflection_agent:
            if spawning_result is not None and isinstance(
                spawning_result, SpawningResult
            ):
                reflection_task = spawning_result.to_reflection_task()
                if reflection_task:
                    reflection_result = self.reflection_agent.execute(reflection_task)

        new_spawning_result = union_the_result_and_the_errors(
            reflection_result.encountered_errors, spawning_result
        )

        self.snapshot = self.snapshot.commit(msg, new_spawning_result)

        return True

    def reset(self, snapshot: Optional[RepoContextSnapshot] = None) -> None:
        """
        Resets the repository to the given snapshot. If no snapshot is provided,
        reset the repo to the current snapshot.
        """
        if snapshot is not None:
            self.snapshot = snapshot

        self.snapshot.reset()

    def reset_to_parent(self) -> None:
        """
        Resets the repository to the parent of the current snapshot. Throws an
        exception if the current snapshot is the initial commit.
        """
        if self.snapshot.parent is None:
            raise Exception("Cannot revert to parent of initial commit")

        self.reset(self.snapshot.parent)

    def reset_to_first(self) -> None:
        """
        Resets the repository to the initial commit.
        """
        while self.snapshot.parent is not None:
            self.reset_to_parent()

    def get_lineage(self) -> list[RepoContextSnapshot]:
        """
        Returns the lineage of the current snapshot, starting from the initial
        commit. The current snapshot is the first element in the list.
        """
        return self.snapshot.lineage


# FIXME: remove this function, only there for the little demo below so the
# pseudo code works
def union_the_result_and_the_errors(*args: Any, **kwargs: Any) -> Any:
    return args[0]


if __name__ == "__main__":
    """
    little demo to show how the class could be used
    """

    def dfs(
        snapshot: RepoContextSnapshot, current: RepoContextSnapshot, depth: int = 0
    ) -> None:
        if current is snapshot:
            print("  " * depth + "> " + f"{snapshot.git_sha[:6]}: {snapshot.msg}")
        else:
            print("  " * depth + ". " + f"{snapshot.git_sha[:6]}: {snapshot.msg}")

        for child in snapshot.children:
            dfs(child, current, depth + 1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)

    args = parser.parse_args()

    manager = RepoContextManager(args.project_root)
    first_snapshot = manager.snapshot

    class Command(StrEnum):
        COMMIT = "commit"
        RESET = "reset"
        UP = "up"
        EXIT = "exit"

    while True:
        print("Current commit tree:")
        dfs(first_snapshot, manager.snapshot)
        print("\n\n")

        cmd = input(f"Enter one of {[e.value for e in Command]}> ")

        try:
            match cmd:
                case Command.COMMIT:
                    manager.commit()
                case Command.RESET:
                    manager.reset()
                case Command.UP:
                    manager.reset_to_parent()
                case Command.EXIT:
                    break
                case _:
                    print("Invalid command")
        except Exception as e:
            print(e)

    print("Goodbye!")
