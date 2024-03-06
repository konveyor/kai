#!/usr/bin/env python

import os
import subprocess  # trunk-ignore(bandit)
import sys

from config import repos, sample_apps


def analyze_apps():
    # perform analysis
    for repo in sample_apps:
        source_dir = sample_apps[repo]
        analyze(source_dir, repo, "initial")

    for repo in repos:
        print(f"Switching to {repos[repo][2]} branch for {repo}...")
        os.chdir(f"sample_repos/{repo}")
        if repos[repo][2] is not None:
            os.system(f"git checkout {repos[repo][2]}")  # trunk-ignore(bandit)
        os.chdir("../../")

    for repo in sample_apps:
        # perform analysis
        source_dir = sample_apps[repo]
        analyze(source_dir, repo, "solved")

    # Our incident_store will expect a app.yaml to exist alongside the
    # analysis reports.  This app.yaml will contain the initial and solved branch info
    for repo in repos:
        data = repos[repo]
        url = data[0]
        initial_branch = data[1]
        solved_branch = data[2]
        update_app_yaml(f"analysis_reports/{repo}", url, initial_branch, solved_branch)


def update_app_yaml(output_dir, url, initial_branch, solved_branch):
    if not os.path.isdir(output_dir):
        sys.exit(
            f"Output directory for app.yaml seems wrong, `{output_dir}` does not exist"
        )
    app_yaml = os.path.join(output_dir, "app.yaml")

    with open(app_yaml, "w") as f:
        f.write(f"initial_branch: {initial_branch}\n")
        f.write(f"solved_branch: {solved_branch}\n")
        f.write(f"repo: {url}\n")


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
    cmd = f'time ./bin/kantra analyze -i {source_dir} -m source-only -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" --rules ./custom_rules -o {full_output_dir} --overwrite'
    subprocess.run(cmd, shell=True)  # trunk-ignore(bandit)


if __name__ == "__main__":
    analyze_apps()
