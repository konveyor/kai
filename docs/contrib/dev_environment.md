# Local Backend Development Environment

This document describes how to setup a local development environment for Kai's
backend.

- [Local Backend Development Environment](#local-backend-development-environment)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Run an analysis of a sample app (example for MacOS)](#run-an-analysis-of-a-sample-app-example-for-macos)
  - [Build and test a local image](#build-and-test-a-local-image)

## Overview

Running Kai's backend involves running a few processes:

- Postgres instance which we deliver via container
- Backend REST API server
- [Optional] Hub Importer process to sync data from Konveyor

## Prerequisites

1. [Python 3.11 or 3.12](https://www.python.org/downloads/)
2. [Podman](https://podman.io/getting-started/installation)
3. Access to a Large Language Model (Note that results vary widely between
   models.)

> [!NOTE]
>
> If you want to run Kai against an LLM you will likely need to configure a LLM
> API key to access your service (unless running against a local model).
>
> We do provide a means of running Kai against previously cached data from a few
> models to aid demo flows. This allows you to run through the steps of using
> Kai without requiring access to a LLM. We call this `KAI__DEMO_MODE`, i.e.
> `KAI__DEMO_MODE=true make run-server`
>
> If you do not provide LLM API access then `KAI__DEMO_MODE` will **only** be
> able to replay previous cached responses.

## Setup

First, clone the repo and ensure you have the virtual environment setup

```sh
git clone https://github.com/konveyor-ecosystem/kai.git
cd kai
python3 -m venv env
source env/bin/activate
pip install pip-tools
pip install -e .
```

Next, open a new terminal run the postgres container via podman:

```sh
make run-postgres
```

Finally, return to your previous terminal run the Kai server:

```sh
make run-server
```

> [!NOTE]
>
> If you want to run with cached LLM responses run with:
> `KAI__DEMO_MODE=true make run-server`. The `KAI__DEMO_MODE` option will cache
> responses and play them back on subsequent runs.
>
> If you want to run with debug information, set the environment variable with:
> `KAI__LOG_LEVEL=debug make run-server`.

On your first run, there will be no solved examples in the database. You can
load some sample data to get started. Open a new terminal and run:

```sh
source env/bin/activate
pushd samples
./fetch_apps.py
popd
make load-data
```

This should complete in ~1-2 minutes.

## Run an analysis of a sample app (example for MacOS)

> [!NOTE]
>
> We have checked in analysis runs for all sample applications so you do NOT
> need to run analysis yourself. The instructions below are ONLY if you want to
> recreate, this is NOT required

Ensure you have the source code for the sample applications checked out locally:

```sh
cd ./samples
./fetch_apps.py
```

This will check out the sample app source code to: `./kai_solution_server/samples/sample_repos`.

Next, run the analysis:

```sh
cd macos
# Sets up the podman VM on MacOS so it will mount the host filesystem into the VM
./restart_podman_machine.sh
# Fetches kantra (our analyzer tool) and stores it in ../bin
./get_latest_kantra_cli.sh
cd ..
# Analyzes all sample apps we know about, in both the 'initial' and 'solved'
# states, expect this to run for ~2-3 hours.
./analyze_apps.py
```

The analysis data will be stored in:
`kai_solution_server/samples/analysis_reports/{APP_NAME}/<initial|solved>/output.yaml`

## Build and test a local image

1. cd to the top level kai checkout
1. Build the local image: `podman build -f build/Containerfile . -t quay.io/konveyor/kai:local`
1. Run: `TAG="local" podman compose up`
1. Then proceed with testing as you want
