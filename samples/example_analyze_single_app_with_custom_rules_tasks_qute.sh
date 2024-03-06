#!/usr/bin/env bash

SOURCE_DIR="tasks-qute"
OUTDIR=${PWD}/analysis_reports/${SOURCE_DIR}
mkdir -p "${OUTDIR}"
time ./bin/kantra analyze -i "${PWD}"/sample_repos/"${SOURCE_DIR}" -m source-only -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" --rules ./custom_rules -o "${OUTDIR}" --overwrite
