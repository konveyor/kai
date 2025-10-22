#!/usr/bin/env bash

SOURCE_NAME=cmt
SOURCE_DIR=${PWD}/../../../kai_solution_server/samples/sample_repos/${SOURCE_NAME}
OUTDIR=${PWD}/${SOURCE_NAME}
mkdir -p "${OUTDIR}"
# Ensure we are on the branch PRIOR to migration
pushd .
cd "${SOURCE_DIR}" || exit
git checkout main
popd || exit
time ../../../kai_solution_server/samples/bin/kantra analyze -i "${SOURCE_DIR}" -t 'quarkus' -t 'jakarta-ee' -t 'jakarta-ee8+' -t 'jakarta-ee9+' -t 'cloud-readiness' --rules ./custom_rules/01-jms-to-reactive-quarkus.windup.yaml -o "${OUTDIR}" --overwrite

# On M1 Max, it took ~3 minutes to run the analysis
#real	3m3.498s
#user	0m0.145s
# sys	0m0.179s
