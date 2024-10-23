#!/bin/sh

mkdir -p ../bin
: ${TAG="latest"}
podman pull quay.io/konveyor/kantra:"${TAG}" && podman run --name kantra-download quay.io/konveyor/kantra:"${TAG}" 1>/dev/null 2>/dev/null && podman cp kantra-download:/usr/local/bin/darwin-kantra ../bin/kantra && podman rm kantra-download
