#!/bin/sh

COVERAGE_REPORT_DIR="${COVERAGE_REPORT_DIR:-htmlcov}"
COVERAGE_ARGS="${COVERAGE_ARGS:---branch}"
UNITTEST_ARGS="${UNITTEST_ARGS-}"

python -m coverage run "${COVERAGE_ARGS}" -m unittest discover "${UNITTEST_ARGS}"
test_result=$?

python -m coverage html --skip-empty -d "${COVERAGE_REPORT_DIR}"

exit "${test_result}"
