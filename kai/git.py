__all__ = ["GitHelper"]

import logging
import os

import git


class GitHelper:
    def __init__(
        self, repo_url, repo_path, initial_branch, solved_branch, old_commit, new_commit
    ):
        self.repo = repo_url
        self.repo_path = repo_path
        self.initial_branch = initial_branch
        self.solved_branch = solved_branch
        self.old_commit = old_commit
        self.new_commit = new_commit
        self.repository = git.Repo(self.repo_path)

    def clone_repo(self, repo_url, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        git.Repo.clone_from(repo_url, dest_dir)

    def get_diff(self):
        # check if the repo_path exists with the code
        if os.path.exists(self.repo_path):
            print(f"Repo path {self.repo_path} exists!! Using local repository")
            repo = git.Repo(self.repo_path)
            # fetch the latest
            repo.remotes.origin.fetch()
        else:
            print(f"Repo path {self.repo_path} does not exist!! Cloning the repository")
            self.clone_repo(self.repo, self.repo_path)
            repo = git.Repo(self.repo_path)

        try:
            # check if the branch exists
            # assuming all the changes are availble in one branch
            repo.git.checkout(self.solved_branch)
            old_commit = repo.commit(self.old_commit)
            new_commit = repo.commit(self.new_commit)
            diff = old_commit.diff(new_commit)
        except Exception as e:
            print(f"Error: {e}")

        return diff

    def get_patch(self, start_commit_id, end_commit_id="HEAD"):
        # If either commit_id is not valid, this will raise a BadName exception
        start_commit = self.repository.commit(start_commit_id)
        end_commit = self.repository.commit(end_commit_id)
        return start_commit.diff(end_commit, create_patch=True)

    def get_patch_for_file(self, file_path, start_commit_id, end_commit_id):
        if file_path.endswith(".svg"):
            return None
        print(
            f"Getting patch for {file_path} between {start_commit_id} and {end_commit_id}"
        )
        diff_indexes = self.get_patch(start_commit_id, end_commit_id)
        # We need to search through the indexes to find the diff for our file_path
        patch = None
        for diff in diff_indexes:
            if diff.a_path == file_path or diff.b_path == file_path:
                patch = diff.diff
                patch = patch.decode("utf-8")
                break
        return patch

    def get_file_contents(self, file_path, commit_id="HEAD"):
        logging.debug(f"Getting file contents for {file_path} in {commit_id}")
        commit = self.repo.commit(commit_id)
        logging.debug(f"Commit: {commit}")
        tree = self.repo.tree(commit)
        logging.debug(f"Tree: {tree}")
        blob = tree[file_path]
        logging.debug(f"Blob: {blob}")
        return blob.data_stream.read().decode()

    def diff_exists_for_file(self, file_path):
        """
        Checks if a diff exists for the specified file path between the provided commit IDs.
        """

        # Get the patch for the file between the two commits
        patch = self.get_patch_for_file(file_path, self.old_commit, self.new_commit)
        # If patch is not None, it means a diff exists for the file
        if patch is not None:
            return True
        else:
            return False
