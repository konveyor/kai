# Local Backend Development Environment

This document describes how to setup a local development environment for Kai's
backend.

- [Local Backend Development Environment](#local-backend-development-environment)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Steps](#steps)
  - [How to use Kai?](#how-to-use-kai)
    - [Ensure you have the source code for the sample applications checked out locally](#ensure-you-have-the-source-code-for-the-sample-applications-checked-out-locally)
      - [(OPTIONAL) Run an analysis of a sample app (example for MacOS)](#optional-run-an-analysis-of-a-sample-app-example-for-macos)
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

1. `git clone https://github.com/konveyor-ecosystem/kai.git`
2. `cd kai`
3. `python3 -m venv env`
4. `source env/bin/activate`
5. `pip install pip-tools`
6. `pip-compile --allow-unsafe`
7. `pip install -r requirements.txt`
8. `pip install -e .`

#### Steps

1. Run the Postgres DB via podman
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-postgres`
1. Run the Kai server in background
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-server`
      - If you want to run with cached LLM responses run with `KAI__DEMO_MODE=true`
        - Replace the above command and instead run: `KAI__DEMO_MODE=true make run-server`
        - The `KAI__DEMO_MODE` option will cache responses and play them back on subsequent runs.
      - If you want to run with debug information set the environment variable `KAI__LOG_LEVEL=debug`
        - Example: `KAI__LOG_LEVEL=debug make run-server`
1. Load data into the database
   1. `source env/bin/activate`
   1. Fetch sample apps: `pushd samples; ./fetch_apps.py; popd`
   1. `make load-data`
      - This will complete in ~1-2 minutes

## How to use Kai?

### Ensure you have the source code for the sample applications checked out locally

1. `cd ./samples`
2. `./fetch_apps.py`
   - This will checkout the sample app source code to: `./samples/sample_repos`
     - This directory is in .gitignore

#### (OPTIONAL) Run an analysis of a sample app (example for MacOS)

Note: We have checked in analysis runs for all sample applications so you do NOT need to run analysis yourself. The instructions below are ONLY if you want to recreate, this is NOT required

1. Install [podman](https://podman.io/) so you can run [Kantra](https://github.com/konveyor/kantra) for static code analysis
1. `cd samples`
1. `./fetch_apps.py` # this will git clone example source code apps
1. `cd macos`
1. `./restart_podman_machine.sh` # setups the podman VM on MacOS so it will mount the host filesystem into the VM
1. `./get_latest_kantra_cli.sh` # fetches 'kantra' our analyzer tool and stores it in ../bin
1. `cd ..`
1. `./analyze_apps.py` # Analyzes all sample apps we know about, in both the 'initial' and 'solved' states, expect this to run for ~2-3 hours.

Analysis data will be stored in: `samples/analysis_reports/{APP_NAME}/<initial|solved>/output.yaml`

## Build and test a local image

1. cd to the top level kai checkout
1. Build: `podman build -f build/Containerfile . -t quay.io/konveyor/kai:local`
1. Run: `TAG="local" podman compose up`
1. Then proceed with testing as you want
