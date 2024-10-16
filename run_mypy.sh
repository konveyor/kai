#!/bin/sh

echo "Running mypy..."
mypy kai
mypy_result=$?
if [ "${mypy_result}" -ne 0 ]; then
	echo "mypy failed.."
	exit "${mypy_result}"
fi

echo "mypy passed."
exit "${mypy_result}"
