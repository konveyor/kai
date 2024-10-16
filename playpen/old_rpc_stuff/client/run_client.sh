#!/usr/bin/env sh

EXAMPLE_HOME="../../example"
SAMPLE_ANALYSIS_REPORT="${EXAMPLE_HOME}/analysis/coolstore/output.yaml"
python3 ./cli.py --report-path "${SAMPLE_ANALYSIS_REPORT}" "${EXAMPLE_HOME}"/coolstore
