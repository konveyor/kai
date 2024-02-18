import os
import pprint
import shutil
import tempfile
import unittest

from git import Repo
from git.exc import GitCommandError, NoSuchPathError

from kai.scm import GitDiff


class TestGitDiff(unittest.TestCase):
    def __init__(self, x):
        super().__init__(x)
        self.pp = pprint.PrettyPrinter(indent=2)
        self.my_dir = os.path.dirname(os.path.realpath(__file__))
        self.remote_cmt_git_url = "https://github.com/konveyor-ecosystem/cmt.git"

    def setUp(self):
        super().setUp()
        # - One of the issues we are facing is when we check out a repo that has remote branches,
        # . those remote branches are not usable until we've checked them out.
        # . To aid testing this we will start with a fresh checkout of a small repo so we can
        # . be sure we are handling the initial case correctly
        #
        # Create a new temporary directory
        self.cmt_tmp_dirpath = tempfile.mkdtemp()
        # Checkout the remote git repo
        # We don't intend to use this repo object we are creating, yet we want to
        # populate the local directory with the remote contents
        Repo.clone_from(self.remote_cmt_git_url, self.cmt_tmp_dirpath)
        # print(f"Cloned '{self.remote_cmt_git_url}' to '{self.cmt_tmp_dirpath}'")
        return

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.cmt_tmp_dirpath)
        # print(f"Removed '{self.cmt_tmp_dirpath}'")
        return

    def get_cmt_repo_path(self):
        return self.cmt_tmp_dirpath

    def test_open_git_repo(self):
        cmt_repo_path = self.get_cmt_repo_path()
        cmt_gd = GitDiff(cmt_repo_path)
        self.assertTrue(cmt_gd is not None)

    def test_open_git_repo_with_error(self):
        with self.assertRaises(NoSuchPathError):
            GitDiff("./bad_non_exsitent_path")

    def test_get_branches(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)
        branches = gd.get_branches()
        self.assertTrue(len(branches) == 1)
        self.assertTrue("main" in branches)

        gd.checkout_branch("quarkus")
        branches = gd.get_branches()
        self.assertTrue(len(branches) == 2)
        self.assertTrue("main" in branches)
        self.assertTrue("quarkus" in branches)

        # Verify we can checkout a branch already checked out with no exception
        gd.checkout_branch("quarkus")
        gd.checkout_branch("quarkus")

    def test_get_file_contents(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)
        file_contents = gd.get_file_contents(
            "src/main/java/org/jboss/as/quickstarts/cmt/model/Customer.java"
        )
        self.assertTrue(
            "public class Customer implements Serializable {" in file_contents
        )

    def test_get_file_contents_with_bad_path(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)
        with self.assertRaises(KeyError):
            # KeyError: "Blob or Tree named 'bad' not found"
            gd.get_file_contents("bad/path/to/file.java")

    def test_checkout_branch_bad_branch(self):
        with self.assertRaises(GitCommandError):
            cmt_path = self.get_cmt_repo_path()
            gd = GitDiff(cmt_path)
            # git.exc.GitCommandError: Cmd('git') failed due to: exit code(1)
            # cmdline: git checkout BAD_BRANCH_NAME
            # stderr: 'error: pathspec 'BAD_BRANCH_NAME' did not match any file(s) known to git'
            gd.checkout_branch("BAD_BRANCH_NAME")

    def test_get_file_contents_from_branch(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)
        file_contents_main_branch = gd.get_file_contents_from_branch(
            "src/main/java/org/jboss/as/quickstarts/cmt/model/Customer.java", "main"
        )
        self.assertTrue(
            "import javax.persistence.GeneratedValue;" in file_contents_main_branch
        )

        with self.assertRaises(IndexError):
            # IndexError: No item found with id 'quarkus'
            file_contents_quarkus_branch = gd.get_file_contents_from_branch(
                "src/main/java/org/jboss/as/quickstarts/cmt/model/Customer.java",
                "quarkus",
            )

        gd.checkout_branch("quarkus")
        file_contents_quarkus_branch = gd.get_file_contents_from_branch(
            "src/main/java/org/jboss/as/quickstarts/cmt/model/Customer.java", "quarkus"
        )
        self.assertTrue(
            "import jakarta.persistence.GeneratedValue;" in file_contents_quarkus_branch
        )

    def test_get_commit_from_branch(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)
        commit_id = gd.get_commit_from_branch("main")
        self.assertTrue(commit_id is not None)
        self.assertTrue(commit_id.hexsha is not None)
        # We expect this is latest commit in 'main':
        # https://github.com/konveyor-ecosystem/cmt/commit/c0267672ffab448735100996f5ad8ed814c38847
        self.assertEqual(commit_id.hexsha, "c0267672ffab448735100996f5ad8ed814c38847")
        commit = gd.repo.commit("c0267672ffab448735100996f5ad8ed814c38847")
        self.assertEqual(commit_id, commit)

        # We expect we can't access the remote quarkus branch unless we've checked it out
        with self.assertRaises(IndexError):
            # IndexError: No item found with id 'quarkus'
            commit_id = gd.get_commit_from_branch("quarkus")

        # Checkout remote quarkus branch so we can move forward
        gd.checkout_branch("quarkus")
        # We expect this is latest commit in 'quarkus':
        # https://github.com/konveyor-ecosystem/cmt/commit/25f00d88f8bceefb223390dcdd656bd5af45146e
        commit_id = gd.get_commit_from_branch("quarkus")
        self.assertTrue(commit_id is not None)
        self.assertTrue(commit_id.hexsha is not None)
        self.assertEqual(commit_id.hexsha, "25f00d88f8bceefb223390dcdd656bd5af45146e")
        commit = gd.repo.commit("25f00d88f8bceefb223390dcdd656bd5af45146e")
        self.assertEqual(commit_id, commit)

    def test_get_commits_for_file(self):
        cmt_path = self.get_cmt_repo_path()
        gd = GitDiff(cmt_path)

        file_path = "src/main/java/org/jboss/as/quickstarts/cmt/mdb/HelloWorldMDB.java"
        # The diff we want should look like:
        # https://github.com/konveyor-ecosystem/cmt/commit/25f00d88f8bceefb223390dcdd656bd5af45146e#diff-e44ebac2ce3d7ebbddf76166dc470f78fe7055554a4e833d35c67981da224117

        start_commit_id = gd.get_commit_from_branch("main").hexsha
        self.assertEqual(start_commit_id, "c0267672ffab448735100996f5ad8ed814c38847")

        # Checkout remote quarkus branch so we can move forward
        gd.checkout_branch("quarkus")

        end_commit_id = gd.get_commit_from_branch("quarkus").hexsha
        self.assertEqual(end_commit_id, "25f00d88f8bceefb223390dcdd656bd5af45146e")

        patch = gd.get_patch_for_file(start_commit_id, end_commit_id, file_path)
        self.assertTrue(patch is not None)
        # print(f"Patch for '{file_path}' between '{start_commit_id}' and '{end_commit_id}':\n{patch}")

        patch_starts_with = "@@ -16,14 +16,10 @@"
        self.assertTrue(patch.startswith(patch_starts_with))
        self.assertTrue("+@ApplicationScoped" in patch)
