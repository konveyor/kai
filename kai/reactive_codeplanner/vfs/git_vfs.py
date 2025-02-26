import argparse
import tempfile
from enum import StrEnum
from pathlib import Path
from typing import Any, Optional

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import AgentResult
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionAgent
from kai.reactive_codeplanner.vfs.repo_context_snapshot import RepoContextSnapshot
from kai.reactive_codeplanner.vfs.spawning_result import SpawningResult

log = get_logger(__name__)


class RepoContextManager:
    def __init__(
        self,
        project_root: Path,
        reflection_agent: Optional[ReflectionAgent] = None,
        initial_msg: str | None = None,
        snapshot_work_dir: Path | None = None,
    ):
        if snapshot_work_dir is None:
            snapshot_work_dir = Path(
                tempfile.TemporaryDirectory(delete=False).name
            ).resolve()

        self.project_root = project_root
        self.snapshot = RepoContextSnapshot.initialize(
            project_root,
            snapshot_work_dir,
            initial_msg,
        )
        self.first_snapshot = self.snapshot
        self.reflection_agent = reflection_agent

    def commit(
        self,
        msg: str | None = None,
        spawning_result: SpawningResult | None = None,
        run_reflection_agent: bool = True,
    ) -> bool:
        """
        Commits the current state of the repository and updates the snapshot.
        Also runs the reflection agent validate the repository state.
        """

        if run_reflection_agent:
            reflection_result = AgentResult()
            if self.reflection_agent:
                if spawning_result is not None and isinstance(
                    spawning_result, SpawningResult
                ):
                    reflection_task = spawning_result.to_reflection_task()
                    if reflection_task:
                        reflection_result = self.reflection_agent.execute(
                            reflection_task
                        )

            union_the_result_and_the_errors(
                reflection_result.encountered_errors, spawning_result
            )
        else:
            pass

        self.snapshot = self.snapshot.commit(msg)

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
