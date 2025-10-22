#!/bin/sh

# Ensure that the script is being executed in the kai/example directory
if [ ! -f "dangerously_reset_coolstore.sh" ]; then
	echo "Please execute this script from the kai/example directory"
	exit 1
fi

cd coolstore || exit

printf "\033[34mHard resetting the coolstore repository to main\033[0m\n"
printf "\033[34m$ git reset --hard main\033[0m\n"
git reset --hard main

printf "\033[34mCleaning untracked files and directories\033[0m\n"
printf "\033[34m$ git clean -fd\033[0m\n"
git clean -fd

printf "\033[34mSetting HEAD to main\033[0m\n"
printf "\033[34m$ git checkout main\033[0m\n"
git checkout main

cd ..
