#!/bin/sh

echo "Running mypy..."
mypy kai kai_solution_server example/run_demo.py --exclude=kai_solution_server/samples.*
mypy_result=$?
if [ "${mypy_result}" -ne 0 ]; then
	echo "mypy failed.."
	exit "${mypy_result}"
fi

echo "mypy passed."
exit "${mypy_result}"
