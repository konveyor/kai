#!/usr/bin/sh

COVERAGE_REPORT_DIR="${COVERAGE_REPORT_DIR:-htmlcov}"

python -m coverage run --branch -m unittest discover
test_result=$?

python -m coverage html --skip-empty -d "${COVERAGE_REPORT_DIR}"

exit "${test_result}"
