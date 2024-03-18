#!/usr/bin/env bash

SOURCE_DIR="tasks-qute"

SOURCE_ONLY=""
# If you want to run with source only uncomment below
# SOURCE_ONLY="-m source-only"

# Choose to either analyze the initial or solved branch
# Then comment out/in the appropriate below
BRANCH="main"
OUTDIR=${PWD}/tmp/${SOURCE_DIR}/initial

#BRANCH="quarkus"
#OUTDIR=${PWD}/tmp/${SOURCE_DIR}/solved

# ####
# Ensure we are on the expected branch before analysis.
# We are typically working with 2 branches an initial/solved
# It's been a common problem to forget which and create invalid analysis runs
# ####
pushd .
cd "${PWD}"/sample_repos/"${SOURCE_DIR}" || exit
git checkout "${BRANCH}"
popd || exit

mkdir -p "${OUTDIR}"
time ./bin/kantra analyze -i "${PWD}"/sample_repos/"${SOURCE_DIR}" "${SOURCE_ONLY}" -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" --rules ./custom_rules -o "${OUTDIR}" --overwrite
