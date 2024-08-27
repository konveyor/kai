#!/usr/bin/bash

PREFIX="/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah"
ANALYSIS_REPORTS_DIR="$PREFIX/samples/analysis_reports"

# for each folder in the analysis_reports directory
for folder in $ANALYSIS_REPORTS_DIR/*; do
	# if the folder is a directory
	if [ -d "$folder" ]; then
		# remove PREFIX from $folder
		no_prefix=${folder#$PREFIX/}

		rm -rf "$folder/initial/static-report"
		git add .
		git commit -s -m "Removed $no_prefix/initial/static-report"

		rm -rf "$folder/solved/static-report"
		git add .
		git commit -s -m "Removed $no_prefix/solved/static-report"

		# wait for input
		# read -p "Press enter to continue"
	fi
done
