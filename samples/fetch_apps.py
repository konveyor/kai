#!/usr/bin/env python

import os
import subprocess  # trunk-ignore(bandit)
import sys

from config import repos


# clone the sample apps in the sample_repos directory
def fetch_sample_apps():
    for repo in repos:
        print(f"Cloning {repo}...")
        gitCloneStatus = subprocess.run(  # trunk-ignore(bandit)
            ["git", "clone", repos[repo][0], f"sample_repos/{repo}"]
        )
        if gitCloneStatus.returncode != 0:
            print(f"Error cloning {repo}")
            print(f"*** Exiting since we couldnt clone '{repo}'")
            sys.exit(1)
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][1] is not None:
            print(f"Debug: git checkout {repos[repo][1]}")
            os.system(f"git checkout {repos[repo][1]}")  # trunk-ignore(bandit)
            os.system(f"git checkout {repos[repo][2]}")  # trunk-ignore(bandit)
        os.chdir("../../")


if __name__ == "__main__":
    # Recommendation:   Don't run this script while VSCode is open and has
    # 'kai' loaded.  I (John M.) spent hours debugging why this script on
    # occasion would fail to checkout the files, looked like a race condition
    # where sometimes we couldn't do a git checkout as the repo name already
    # existed as a directory with just a few files under 'target' similar to
    # below:
    #   https://gist.github.com/jwmatthews/6becd1b46237352ad9cdaf74f11a7cd4
    # finally realized, while the 'kai' source code was open in VSCode the Java
    # analyzer was continuing to analyzing the sample apps, and as I was
    # deleting/checking them out for testing, there was a potential race of
    # VSCode, doing a partial compile and updating a few files under target.
    #
    # To move forward, I'll close VSCode before running this script
    fetch_sample_apps()
