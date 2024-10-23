#!/usr/bin/env bash

SOURCE_DIR="cmt"

# Choose to either analyze the initial or solved branch
# Then comment out/in the appropriate below
BRANCH="main"
OUTDIR=${PWD}/tmp/${SOURCE_DIR}/initial

#BRANCH="quarkus"
#OUTDIR=${PWD}/tmp/${SOURCE_DIR}/solved

mkdir -p "${OUTDIR}"

SOURCE_ONLY=""
# If you want to run with source only uncomment below
# SOURCE_ONLY="-m source-only"

# ####
# Ensure we are on the expected branch before analysis.
# We are typically working with 2 branches an initial/solved
# It's been a common problem to forget which and create invalid analysis runs
# ####
pushd .
cd "${PWD}"/sample_repos/"${SOURCE_DIR}" || exit
git checkout "${BRANCH}"
popd || exit

# Run jaeger
podman kill kantrajaeger
podman rm kantrajaeger
podman run -d --name kantrajaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -p 14268:14268 -p 16686:16686 registry.redhat.io/rhosdt/jaeger-all-in-one-rhel8
JAEGER_IP=$(podman inspect kantrajaeger | jq '.[0].NetworkSettings.Networks.podman.IPAddress' | sed 's/^"//; s/"$//') # trunk-ignore(shellcheck)
JAEGER_ENDPOINT="http://${JAEGER_IP}:14268/api/traces"
echo "JAEGER_ENDPOINT=${JAEGER_ENDPOINT}"

time ./bin/kantra analyze -i "${PWD}"/sample_repos/"${SOURCE_DIR}" "${SOURCE_ONLY}" -t "quarkus" -t "jakarta-ee" -t "jakarta-ee8+" -t "jakarta-ee9+" -t "cloud-readiness" --rules ./custom_rules -o "${OUTDIR}" --overwrite --jaeger-endpoint "${JAEGER_ENDPOINT}"

# To get metrics
curl -o ./tmp/traces.json "http://localhost:16686/api/traces?service=analyzer-lsp"
