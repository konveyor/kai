# Getting Started

- [Getting Started](#getting-started)
  - [Overview](#overview)
  - [Recommended path - use `podman compose up` with cached LLM responses](#recommended-path---use-podman-compose-up-with-cached-llm-responses)
    - [Launch Kai with sample data and cached LLM responses](#launch-kai-with-sample-data-and-cached-llm-responses)
    - [Next interact with Kai via a Guided Walkthrough Scenario](#next-interact-with-kai-via-a-guided-walkthrough-scenario)
      - [What are the general steps of Kai's current evaluation demo?](#what-are-the-general-steps-of-kais-current-evaluation-demo)
  - [Alternative methods of running](#alternative-methods-of-running)
    - [With data from Konveyor Hub](#with-data-from-konveyor-hub)
    - [Development Environment](#development-environment)
    - [Example CLI Script in Python](#example-cli-script-in-python)
  - [Misc notes](#misc-notes)
    - [Extending the data Kai consumes](#extending-the-data-kai-consumes)
    - [Misc notes with `podman compose`](#misc-notes-with-podman-compose)

## Overview

Running Kai consists of:

1. Launching a postgres database and seed with application analysis data
1. Launching the backend Kai REST API Service
   - This is the component that will work with the database, construct prompts,
     talk to Large Language Models (LLMs), and generate code fixes
1. A client that parses analysis information from
   [analyzer-lsp](https://github.com/konveyor/analyzer-lsp) and then issues
   requests to the Kai backend.
   - The primary client will be an IDE plugin
     - For IDE setup see: [Install the Kai VSCode
       Plugin](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md)
   - It's also possible to issue API requests directly, and we have a python
     script that does this to aid demonstrations. See
     [example/README.md](/example/README.md)

## Recommended path - use `podman compose up` with cached LLM responses

The easiest way to run Kai is to leverage the prebuilt container images
we publish to
[quay.io/konveyor/kai](https://quay.io/repository/konveyor/kai?tab=tags), you
can learn more about early builds at
[docs/evaluation_builds.md](/docs/evaluation_builds.md).

This is the simplest configuration which will limit configuration choices and will use cached LLM results so that you may evaluate Kai without having your own API Keys.

- The cached data uses a `KAI__DEMO_MODE=TRUE` mode for running the backend. See [docs/contrib/configuration.md](/docs/contrib/configuration.md) for more information.
- Follow the guided scenario at [docs/scenarios/demo.md](/docs/scenarios/demo.md) to evaluate Kai

### Launch Kai with sample data and cached LLM responses

_This will run Kai using [sample analysis reports](/samples/analysis_reports) that simulates the analysis data which will be obtained from Konveyor. Additionally it will default to using cached LLM responses as explained in [docs/contrib/configuration.md](/docs/contrib/configuration.md)_

Steps:

1. `git clone https://github.com/konveyor/kai.git`
1. `cd kai`
1. Optional Configuration changes _ok to skip and use the defaults if using cached responses_
   1. Make changes to `kai/config.toml` to select your desired provider and model
   1. Export `GENAI_KEY` or `OPENAI_API_KEY` as appropriate as per [docs/llm_selection.md](/docs/llm_selection.md)
   1. Note: By default the `stable` image tag will be used by podman compose.yaml. If you want to run with an alternate tag you can export the environment variable: `TAG="stable"` with any tag you would like to use.
1. Run `podman compose up`. The first time this is run it will take several minutes to download images and to populate sample data.
   - After the first run the DB will be populated and subsequent starts will be much faster, as long as the kai_kai_db_data volume is not deleted.
   - To clean up all resources run `podman compose down && podman volume rm kai_kai_db_data`.
1. Kai backend is now running and ready to serve requests

### Next interact with Kai via a Guided Walkthrough Scenario

For an initial evaluation, the recommended path is to follow a guided walkthrough we have created at: [docs/scenarios/demo.md](docs/scenarios/demo.md) which walks through a scenario of using Kai to complete a migration of a Java EE app to Quarkus.

#### What are the general steps of Kai's current evaluation demo?

1. We launch VSCode with our Kai VS Code extension from [konveyor-ecosystem/kai-vscode-plugin](https://github.com/konveyor-ecosystem/kai-vscode-plugin/tree/main)
2. We open a git checkout of a sample application: [coolstore](https://github.com/konveyor-ecosystem/coolstore)
3. We run [Kantra](https://github.com/konveyor/kantra) inside of VSCode to do an analysis of the application to learn what issues are present that need to be addressed before migrating to Quarkus
4. We view the analysis information in VSCode
5. We look at the impacted files and choose what files/issues we want to fix
6. We click 'Generate Fix' in VSCode on a given file/issue and wait ~45 seconds for the Kai backend to generate a fix
7. We view the suggested fix as a 'Diff' in VSCode
8. We accept the generated fix
9. The file in question has now been updated
10. We move onto the next file/issue and repeat

## Alternative methods of running

### With data from Konveyor Hub

_Konveyor integration is still being developed and is not yet fully integrated._

1. `git clone https://github.com/konveyor-ecosystem/kai.git`
1. `cd kai`
1. Make changes to `kai/config.toml` to select your desired provider and model
1. Export `GENAI_KEY` or `OPENAI_API_KEY` as appropriate
1. Run `USE_HUB_IMPORTER=True HUB_URL=https://tackle-konveyor-tackle.apps.cluster.example.com/hub IMPORTER_ARGS=-k podman compose --profile use_hub_importer up`
   - Note you will want to update the value of `HUB_URL` to match your Konveyor cluster

### Development Environment

You may also run the Kai server from a python virtual environment to aid testing local changes without needing to build a container image.

- See [docs/contrib/dev_environment.md](/docs/contrib/dev_environment.md)

### Example CLI Script in Python

- See [docs/example_cli_script.md](/docs/archived/example_cli_script.md) to see an alternative method of running the development team uses to exercise the Kai REST API from a python script

## Misc notes

### Extending the data Kai consumes

- You may modify the analysis information Kai consumes via [docs/custom_apps.md](/docs/archived/custom_apps.md)

### Misc notes with `podman compose`

Note that you need to use podman >= 1.1.0 to use the `--profile` option. podman does not currently support the alternative `COMPOSE_PROFILES` environment variable.

If your konveyor instance does not use self-signed certificates you may omit `IMPORTER_ARGS=-k`.

To clean up all resources run `podman compose --profile use_hub_importer down && podman volume rm kai_kai_db_data`.
