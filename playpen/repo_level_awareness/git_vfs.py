import argparse
import functools
import logging
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Optional

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)


# NOTE: I'd like to use GitPython, but using custom a work-tree and git-dir with
# it is too hard.
@dataclass(frozen=True)
class GitVFSSnapshot:
    work_tree: Path  # project root
    git_dir: Path
    git_sha: str

    parent: Optional["GitVFSSnapshot"] = None
    children: list["GitVFSSnapshot"] = field(default_factory=list)

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

    def git(self, args: list[str], popen_kwargs: dict[str, Any] | None = None):
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
        proc = subprocess.Popen(GIT + args, **popen_kwargs)
        stdout, stderr = proc.communicate()

        log.debug(f"\033[94mreturncode:\033[0m {proc.returncode}")
        log.debug(f"\033[94mstdout:\033[0m\n{stdout}")
        log.debug(f"\033[94mstderr:\033[0m\n{stderr}")

        return proc.returncode, stdout, stderr

    @staticmethod
    def initialize(work_tree: Path) -> "GitVFSSnapshot":
        """
        Creates a new git repo in the given work_tree, and returns a
        GitVFSSnapshot.
        """
        work_tree = work_tree.resolve()
        kai_dir = work_tree / ".kai"
        kai_dir.mkdir(exist_ok=True)
        git_dir = kai_dir / f".git-{datetime.now(timezone.utc).isoformat()}"

        # Snapshot is immutable, so we create a temporary snapshot to get the
        # git sha of the initial commit
        tmp_snapshot = GitVFSSnapshot(
            work_tree=work_tree,
            git_dir=git_dir,
            git_sha="",
        )

        returncode, _, stderr = tmp_snapshot.git(["init"])
        if returncode != 0:
            raise Exception(f"Failed to initialize git repository: {stderr}")

        with open(git_dir / "info" / "exclude", "a") as f:
            f.write(f"/{str(kai_dir.name)}\n")

        tmp_snapshot = tmp_snapshot.commit("Initial commit")

        return GitVFSSnapshot(
            work_tree=work_tree,
            git_dir=git_dir,
            git_sha=tmp_snapshot.git_sha,
            parent=None,
            children=[],
        )

    def commit(self, msg: str | None = None) -> "GitVFSSnapshot":
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

        result = GitVFSSnapshot(
            work_tree=self.work_tree,
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


if __name__ == "__main__":
    """
    little demo to show how the class could be used
    """

    def dfs(snapshot: GitVFSSnapshot, current: GitVFSSnapshot, depth: int = 0):
        if current is snapshot:
            print("  " * depth + "> " + f"{snapshot.git_sha[:6]}: {snapshot.msg}")
        else:
            print("  " * depth + ". " + f"{snapshot.git_sha[:6]}: {snapshot.msg}")

        for child in snapshot.children:
            dfs(child, current, depth + 1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)

    args = parser.parse_args()

    first_snapshot = GitVFSSnapshot.initialize(args.project_root)
    snapshot = first_snapshot

    class Command(StrEnum):
        COMMIT = "commit"
        RESET = "reset"
        UP = "up"
        EXIT = "exit"

    while True:
        print("Current commit tree:")
        dfs(first_snapshot, snapshot)
        print("\n\n")

        cmd = input(f"Enter one of {[e.value for e in Command]}> ")
        match cmd:
            case Command.COMMIT:
                snapshot = snapshot.commit()
            case Command.RESET:
                snapshot.reset()
            case Command.UP:
                if snapshot.parent is None:
                    print("Cannot revert to parent of initial commit")
                    continue

                snapshot = snapshot.parent
                snapshot.reset()
            case Command.EXIT:
                break
            case _:
                print("Invalid command")

    print("Goodbye!")