# Getting Started

## Overview

Running Kai consists of:

1. Launching the backend Kai REST API Service
   - This the component that will construct prompts, talk to Large Language Models (LLMs), and generate code fixes
1. A client that parses analysis information from [Kantra](https://github.com/konveyor/kantra) and then issues requests to the Kai backend.
   - The primary client will be an IDE plugin
   - It's also possible to issue API requests directly, and we have a python script that does this to aid demonstrations. See [example/README.md](example/README.md)

## `podman compose up`

- The easiest way to run is to leverage prebuilt container images we publish to [quay.io/konveyor/kai](https://quay.io/repository/konveyor/kai?tab=tags), you can learn more about early builds at [docs/Evaluation_Builds.md](docs/Evaluation_Builds.md)

### With sample data

- This will run Kai using [sample data](samples/analysis_reports) that simulates the analysis data which will be obtained from Konveyor.

1. `git clone https://github.com/konveyor/kai.git`
1. `cd kai`
1. Make changes to `kai/config.toml` to select your desired provider and model
1. Export `GENAI_KEY` or `OPENAI_API_KEY` as appropriate as per [docs/LLM_Selection.md](docs/LLM_Selection.md)
1. Run `podman compose up`. The first time this is run it will take several minutes to download images and to populate sample data.
   - After the first run the DB will be populated and subsequent starts will be much faster, as long as the kai_kai_db_data volume is not deleted.
   - To clean up all resources run `podman compose down && podman volume rm kai_kai_db_data`.
1. Kai backend is now running and ready to serve requests

### With data from Konveyor Hub

_Konveyor integration is still being developed and is not yet fully integrated._

1. `git clone https://github.com/konveyor-ecosystem/kai.git`
1. `cd kai`
1. Make changes to `kai/config.toml` to select your desired provider and model
1. Export `GENAI_KEY` or `OPENAI_API_KEY` as appropriate
1. Run `USE_HUB_IMPORTER=True HUB_URL=https://tackle-konveyor-tackle.apps.cluster.example.com/hub IMPORTER_ARGS=-k podman compose --profile use_hub_importer up`

### Misc notes with `podman compose`

Note that you need to use podman >= 1.1.0 to use the `--profile` option. podman does not currently support the alternative `COMPOSE_PROFILES` environment variable.

If your konveyor instance does not use self-signed certificates you may omit `IMPORTER_ARGS=-k`.

To clean up all resources run `podman compose --profile use_hub_importer down && podman volume rm kai_kai_db_data`.

## Development Environment

You may also run the Kai server from a python virtual environment to aid testing local changes without needing to build a container image.

- See [docs/contrib/Dev_Environment.md](docs/contrib/Dev_Environment.md)
