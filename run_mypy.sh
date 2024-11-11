#!/bin/sh

echo "Running mypy..."
mypy kai kai_solution_server --exclude=kai_solution_server/samples.* --namespace-packages
mypy_result=$?
if [ "${mypy_result}" -ne 0 ]; then
	echo "mypy failed.."
	exit "${mypy_result}"
fi

echo "mypy passed."
exit "${mypy_result}"
