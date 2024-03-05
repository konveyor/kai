#!/usr/bin/env python

import os
import subprocess  # trunk-ignore(bandit)

from config import repos


# clone the sample apps in the sample_repos directory
def fetch_sample_apps():
    for repo in repos:
        print(f"Cloning {repo}...")
        subprocess.run(  # trunk-ignore(bandit)
            ["git", "clone", repos[repo][0], f"sample_repos/{repo}"]
        )
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][1] is not None:
            print(f"Debug: git checkout {repos[repo][1]}")
            os.system(f"git checkout {repos[repo][1]}")  # trunk-ignore(bandit)
        os.chdir("../../")


if __name__ == "__main__":
    fetch_sample_apps()
