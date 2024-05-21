# Run Kai with your Applications

Konveyor AI (KAI) leverages LLMs to streamline the modernization of application source code. To learn how Kai works, run this demo <insert demo link></insert>

## Pre-requisites

- Install [podman](https://podman.io/)
- VS Code
- git
- GEN AI Credentials

To run Kai with your Applications, follow these steps

## Configure Application

1. Navigate to the samples folder - `cd samples`
1. In `./samples/config.py`, add your application's info to `repos` dict.

```python
 "<app name>": [
        "https://github.com/<path to repo>",
        "<source branch>",
        "<migrated/target branch>",
    ],
```

- app name : The name of your application.
- path to repo : The full path to your application's repository on GitHub.

- source branch : The branch of the repository that contains the current version of your application code.
- migrated/target branch : The branch that will contain the migrated version of your application code. This is optional and will be used to generate solved examples that can be used to solve similar issues in the future.

Here's an example for an application named exampleApp:

```python
"exampleApp": [
        "https://github.com/exampleOrg/exampleApp.git",
        "develop",  # Source branch
        "migrated",  # Target branch
    ],

```

1. Add your app information to `sample_apps` dict in the same file

```python
"<app_name>" : "sample_repos/<app_name>",
```

for exampleApp, it will be of the format

```python
    "exampleApp" = "sample_repos/exampleApp"
```

Make sure that the git repo is public and accessible. Currently, Kai only supports publicly accessible repos

### Fetch the Application

Once you are done with the above configuration, run

```shell=
./fetch_apps.py
```

This step will clone the repo in the location 'sample_repos'

### Run Analysis

Before running analysis, make sure that you have `kantra` installed

1. `cd macos`
1. `./restart_podman_machine.sh` # setups the podman VM on MacOS so it will mount the host filesystem into the VM
1. `./get_latest_kantra_cli.sh` # fetches 'kantra' our analyzer tool and stores it in ../bin
1. `cd ..`

To run analysis reports for the applications listed in `./samples/config.py`, run

```shell=
./analyze_apps.py
```

This step analyzes all sample apps we know about, in both the 'initial' and 'solved' states, expect this to run for ~2-3 hours.

Analysis data will be stored in: `samples/analysis_reports/{APP_NAME}/<initial|solved>/output.yaml`

### Run Kai server

1. Configure GEN AI key and select model by following these [steps](https://github.com/konveyor-ecosystem/kai/blob/main/README.md#pre-requisites)
2. Run Kai server by following these [steps](https://github.com/konveyor-ecosystem/kai/blob/main/README.md#setup)

### Configure Kai VSCode plugin

1. Install Kai IDE plugin by following these [instructions](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md#ide-plugin-installation-methods)

2. Clone the application you want to analyze and navigate to File > Open in VSCode and locate the folder and open it
3. Run [Kantra analysis](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md#running-kantra-analysis) of the app after selecting the targets you need

4. To fix issues identified during analysis using Kai, follow these [steps](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md#running-kai-fix)
