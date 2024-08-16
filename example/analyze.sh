#!/usr/bin/env bash

SOURCE_DIR="coolstore"

SOURCE_ONLY=""
# If you want to run with source only uncomment below
# SOURCE_ONLY="-m source-only"

# We are experimenting with modifying some of the default Kantra rules from:
# . https://github.com/konveyor/rulesets/tree/main/default/generated
DEFAULT_RULES_DIR="${PWD}/default_rules"

CUSTOM_RULES_DIR="${PWD}/../samples/custom_rules"

# Choose to either analyze the initial or solved branch
# Then comment out/in the appropriate below
BRANCH="main"
OUTDIR=${PWD}/analysis/${SOURCE_DIR}/

#BRANCH="quarkus"
#OUTDIR=${PWD}/tmp/${SOURCE_DIR}/solved

KANTRA_BIN="${PWD}/../samples/bin/kantra"
# CHECK that bin exits, exit if not
if [[ ! -f ${KANTRA_BIN} ]]; then
	echo "Kantra binary not found at ${KANTRA_BIN}"
	echo "Please look at '${CWD}/../samples/macos/get_latest_kantra_cli.sh' for example of how to get Kantra"
	exit 1
fi

# Ensure that the source has been fetched
if [[ ! -d "${PWD}"/"${SOURCE_DIR}" ]]; then
	echo "Source directory not found at ${PWD}/${SOURCE_DIR}"
	echo "Please ensure you checkout the application source code to analyze"
	echo "Run: ./fetch.sh"
	exit 1
fi

# ####
# Ensure we are on the expected branch before analysis.
# We are typically working with 2 branches an initial/solved
# It's been a common problem to forget which and create invalid analysis runs
# ####
pushd .
cd "${PWD}"/"${SOURCE_DIR}" || exit
git checkout "${BRANCH}"
popd || exit

mkdir -p "${OUTDIR}"
# ###
# # John M:
# Commenting out the disable of builtin rules so we can use our modified versions.
# Our modified rules are an experiment, as of 8/16/2024 I am unsure if they provide a benefit
# I'm leaving this snippet of code here commented out instead of removing as this is all
# still experimental and I wanted to leave an explicit trace of this experiment as we may go back to it
# ###
#
#time "${KANTRA_BIN}" analyze -i "${PWD}"/"${SOURCE_DIR}" "${SOURCE_ONLY}" --enable-default-rulesets=false -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8" -t "jakarta-ee9" -t "cloud-readiness" --rules "${DEFAULT_RULES_DIR}" --rules "${CUSTOM_RULES_DIR}" -o "${OUTDIR}" --overwrite

time "${KANTRA_BIN}" analyze -i "${PWD}"/"${SOURCE_DIR}" "${SOURCE_ONLY}" -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8" -t "jakarta-ee9" -t "cloud-readiness" --rules "${CUSTOM_RULES_DIR}" -o "${OUTDIR}" --overwrite
