#!/usr/bin/env python

import os
import subprocess  # trunk-ignore(bandit)
import sys

repos = {
    "eap-coolstore-monolith": [
        "https://github.com/mathianasj/eap-coolstore-monolith.git",
        "main",
        "quarkus-migration",
    ],
    "kitchensink": [
        "https://github.com/tqvarnst/jboss-eap-quickstarts.git",
        "main",
        "quarkus-3.2",
    ],
    "ticket-monster": ["https://github.com/jmle/monolith.git", "master", "quarkus"],
    "jboss-eap-quickstarts": [
        "https://github.com/jboss-developer/jboss-eap-quickstarts",
        "7.4.x",
        None,
    ],
    "jboss-eap-quickstarts-quarkus": [
        "https://github.com/christophermay07/quarkus-migrations",
        "main",
        "main",
    ],
    "helloworld-mdb": [
        "https://github.com/savitharaghunathan/helloworld-mdb.git",
        "main",
        "quarkus",
    ],
    "bmt": ["https://github.com/konveyor-ecosystem/bmt.git", "main", "quarkus"],
    "cmt": ["https://github.com/konveyor-ecosystem/cmt.git", "main", "quarkus"],
}

sample_source_apps = {
    "eap-coolstore-monolith": "sample_repos/eap-coolstore-monolith",
    "ticket-monster": "sample_repos/ticket-monster",
    "kitchensink": "sample_repos/kitchensink",
    "helloworld-mdb": "sample_repos/helloworld-mdb",
    "bmt": "sample_repos/bmt",
    "cmt": "sample_repos/cmt",
    "ejb-remote": "sample_repos/jboss-eap-quickstarts/ejb-remote",
    "ejb-security": "sample_repos/jboss-eap-quickstarts/ejb-security",
    "tasks-jsf": "sample_repos/jboss-eap-quickstarts/tasks-jsf",
}

sample_target_apps = {
    "eap-coolstore-monolith": "sample_repos/eap-coolstore-monolith",
    "ticket-monster": "sample_repos/ticket-monster",
    "kitchensink": "sample_repos/kitchensink",
    "helloworld-mdb": "sample_repos/helloworld-mdb",
    "bmt": "sample_repos/bmt",
    "cmt": "sample_repos/cmt",
    "ejb-remote": "sample_repos/jboss-eap-quickstarts-quarkus/ejb-remote-to-quarkus-rest",
    "ejb-security": "sample_repos/jboss-eap-quickstarts-quarkus/ejb-security-to-quarkus-basic-elytron",
    "tasks-jsf": "sample_repos/jboss-eap-quickstarts-quarkus/tasks-qute",
}


# clone the sample apps in the sample_repos directory
# skip jboss-eap-quickstarts-quarkus
def fetch_sample_apps():
    for repo in repos:
        print(f"Cloning {repo}...")
        os.system(f"git clone {repos[repo][0]} sample_repos/{repo}")
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][1] is not None:
            os.system(f"git checkout {repos[repo][1]}")
        print(f"Current working directory: {os.getcwd()}")
        os.chdir("../../")

        # perform analysis
    for repo in sample_source_apps:
        source_dir = sample_source_apps[repo]
        analyze(source_dir, repo, "initial")

    # switch to quarkus branch and perform analysis again
    # skip jboss-eap-quickstarts
    for repo in repos:
        if repo == "jboss-eap-quickstarts":
            continue
        print(f"Switching to {repos[repo][2]} branch for {repo}...")
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][2] is not None:
            os.system(f"git checkout {repos[repo][2]}")
        os.chdir("../../")

    for repo in sample_target_apps:
        # perform analysis
        source_dir = sample_target_apps[repo]
        analyze(source_dir, repo, "solved")


def ensure_kantra_bin_exists():
    kantra_bin = os.path.join(os.getcwd(), "bin/kantra")
    print(f"Checking for Kantra binary at {kantra_bin}")
    if not os.path.isfile(kantra_bin):
        sys.exit(f"Unable to find {kantra_bin}\nPlease install Kantra")


def ensure_output_dir_exists(output_dir):
    if not os.path.isdir(output_dir):
        print(f"Creating output directory '{output_dir}'")
        # os.mkdir(output_dir)
        os.makedirs(output_dir)


def analyze(source_dir, name, target):
    ensure_kantra_bin_exists()
    full_output_dir = os.path.join(os.getcwd(), f"analysis_reports/{name}/{target}")
    ensure_output_dir_exists(full_output_dir)
    print(f"Analyzing '{source_dir}', will write output to '{full_output_dir}'")
    cmd = f'time ./bin/kantra analyze -i {source_dir} -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" -o {full_output_dir} --overwrite'
    subprocess.run(cmd, shell=True)  # trunk-ignore(bandit)


if __name__ == "__main__":
    fetch_sample_apps()
