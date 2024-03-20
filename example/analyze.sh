#!/usr/bin/env bash

SOURCE_DIR="coolstore"

SOURCE_ONLY=""
# If you want to run with source only uncomment below
# SOURCE_ONLY="-m source-only"

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
time "${KANTRA_BIN}" analyze -i "${PWD}"/"${SOURCE_DIR}" "${SOURCE_ONLY}" -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" --rules "${CUSTOM_RULES_DIR}" -o "${OUTDIR}" --overwrite
