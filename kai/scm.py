__all__ = ["GitDiff"]

import logging
from typing import TYPE_CHECKING

import git
from git import BadName, Repo

if TYPE_CHECKING:
    from git import Commit, Head
    from git.diff import DiffIndex
    from git.util import IterableList

KAI_LOG = logging.getLogger(__name__)


# NOTE(JonahSussman): Types for this file may be incorrect
class GitDiff:
    def __init__(self, repo_path: git.types.PathLike) -> None:
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def get_patch(
        self, start_commit_id: str, end_commit_id: str = "HEAD"
    ) -> DiffIndex[str]:
        # If either commit_id is not valid, this will raise a BadName exception
        start_commit = self.repo.commit(start_commit_id)
        end_commit = self.repo.commit(end_commit_id)
        return start_commit.diff(end_commit_id, create_patch=True)

    def get_patch_for_file(
        self, start_commit_id: str, end_commit_id: str, file_path: str
    ) -> str | None:
        diff_indexes = self.get_patch(start_commit_id, end_commit_id)
        # We need to search through the indexes to find the diff for our file_path
        patch = None
        for diff in diff_indexes:
            # print(f"'{file_path}' '{diff.a_path}' '{diff.b_path}' ")
            if diff.a_path == file_path or diff.b_path == file_path:
                # print("Found match")
                patch = diff.diff
                patch = patch.decode("utf-8")
                break
        return patch

    def get_file_contents(self, file_path: str, commit_id: str = "HEAD") -> str:
        KAI_LOG.debug(f"Getting file contents for {file_path} in {commit_id}")
        commit = self.repo.commit(commit_id)
        KAI_LOG.debug(f"Commit: {commit}")
        tree = self.repo.tree(commit)
        KAI_LOG.debug(f"Tree: {tree}")
        blob = tree[file_path]
        KAI_LOG.debug(f"Blob: {blob}")
        return blob.data_stream.read().decode()

    def get_file_contents_from_branch(
        self, file_path: str, branch: str = "main"
    ) -> str:
        commit_id = self.get_commit_from_branch(branch)
        return self.get_file_contents(file_path, commit_id)

    def get_commits_for_file(self, file_path: str, max_count: int = 10) -> list[Commit]:
        commits_for_file_generator = self.repo.iter_commits(
            all=True, max_count=max_count, paths=file_path
        )
        commits_for_file = list(commits_for_file_generator)
        return commits_for_file

    def get_commit_from_branch(self, branch_name: str) -> Commit:
        return self.repo.heads[str(branch_name)].commit

    def get_branches(self) -> IterableList[Head]:
        return self.repo.heads

    def checkout_branch(self, branch_name: str) -> None:
        self.repo.git.checkout(branch_name)

    def diff_exists_for_file(
        self, old_commit: str, new_commit: str, file_path: str
    ) -> bool | None:
        """
        Checks if a diff exists for the specified file path between the provided commit IDs.
        """
        if file_path.endswith(".svg"):
            return None

        # Get the patch for the file between the two commits
        patch = self.get_patch_for_file(old_commit, new_commit, file_path)
        # If patch is not None, it means a diff exists for the file
        if patch is not None:
            return True
        else:
            return False
