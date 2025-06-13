#!/bin/sh

echo "Running mypy..."
uv run mypy src --enable-error-code unused-awaitable
mypy_result=$?
if [ "${mypy_result}" -ne 0 ]; then
	echo "mypy failed."
	exit "${mypy_result}"
fi

echo "mypy passed."
exit "${mypy_result}"
