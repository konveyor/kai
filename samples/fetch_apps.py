#!/usr/bin/env python

import os
import subprocess  # trunk-ignore(bandit)
import sys

from config import repos, sample_source_apps, sample_target_apps


# clone the sample apps in the sample_repos directory
# skip jboss-eap-quickstarts-quarkus
def fetch_sample_apps():
    for repo in repos:
        print(f"Cloning {repo}...")
        subprocess.run(  # trunk-ignore(bandit)
            ["git", "clone", repos[repo][0], f"sample_repos/{repo}"]
        )
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][1] is not None:
            os.system(f"git checkout {repos[repo][1]}")  # trunk-ignore(bandit)
        os.chdir("../../")


if __name__ == "__main__":
    fetch_sample_apps()
