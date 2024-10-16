#!/bin/sh

COVERAGE_REPORT_DIR="${COVERAGE_REPORT_DIR:-htmlcov}"

echo "Coverage report will be saved to ${COVERAGE_REPORT_DIR}"

echo "Running tests..."
python -m coverage run --branch -m unittest discover --failfast
test_result=$?

python -m coverage html --skip-empty -d "${COVERAGE_REPORT_DIR}"

if [ "${test_result}" -eq 0 ]; then
	echo "Tests passed."
else
	echo "Tests failed."
fi

exit "${test_result}"
