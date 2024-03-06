#!/usr/bin/env bash

apps=("ejb-remote")

for src_name in "${apps[@]}"; do
	src_dir=${PWD}/../../../samples/sample_repos/${src_name}
	outdir=${PWD}/${src_name}
	mkdir -p "${outdir}"
	echo "Analyzing ${src_name} src: ${src_dir} out: ${outdir}"
	# Ensure we are on the branch PRIOR to migration
	pushd .
	cd "${src_dir}" || exit
	git checkout main
	popd || exit
	time ../../../samples/bin/kantra analyze -i "${src_dir}" -m source-only -t 'quarkus' -t 'jakarta-ee' -t 'jakarta-ee8+' -t 'jakarta-ee9+' -t 'cloud-readiness' --rules ./custom_rules -o "${outdir}" --overwrite
done
