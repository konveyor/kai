# Konveyor AI (kai)

Konveyor AI (kai) is Konveyor's approach to easing modernization of application source code to a new target by leveraging LLMs with guidance from static code analysis augmented with data in Konveyor that helps to learn how an Organization solved a similar problem in the past.

Pronunciation of 'kai': https://www.howtopronounce.com/kai

## Blog Posts

- 2024 May 07: [Apply generative AI to app modernization with Konveyor AI](https://developers.redhat.com/articles/2024/05/07/modernize-apps-konveyor-ai)
- 2024 May 07: [Kai - Generative AI Applied to Application Modernization](https://www.konveyor.io/blog/kai-deep-dive-2024/)

## Approach

Our approach is to use static code analysis to find the areas in source code that need to be transformed. 'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

This approach does _not_ require fine-tuning of LLMs, we augment a LLMs knowledge via the prompt, similar to approaches with [RAG](https://arxiv.org/abs/2005.11401) by leveraging external data from inside of Konveyor and from Analysis Rules to aid the LLM in constructing better results.

For example, [analyzer-lsp Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) such as these ([Java EE to Quarkus rulesets](https://github.com/konveyor/rulesets/tree/main/default/generated/quarkus)) are leveraged to aid guiding a LLM to update a legacy Java EE application to Quarkus

Note: For purposes of this initial prototype we are using an example of Java EE to Quarkus. That is an arbitrary choice to show viability of this approach. The code and the approach will work on other targets that Konveyor has rules for.

### What happens technically to make this work?

- [Konveyor](konveyor.io) contains information related to an Organization's Application Portfolio, a view into all of the applications an Organization is managing. This view includes a history of analysis information over time, access to each applications source repositories, and metadata that tracks work in-progress/completed in regard to each application being migrated to a given technology.

- When 'Konveyor AI' wants to fix a specific issue in a given application, it will mine data in Konveyor to extract 2 sources of information to inject into a given LLM prompt.

  1.  Static Code Analysis

      - We pinpoint where to begin work by leveraging static code analysis to guide us
      - The static code analysis is informed via a collection of crowd sourced knowledge contained in our [rulesets](https://github.com/konveyor/rulesets/tree/main) plus augmented via [custom-rules](https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules)
      - We include in the prompt Analysis metadata information to give the LLM more context [such as](https://github.com/konveyor-ecosystem/kai/blob/main/example/analysis/coolstore/output.yaml#L2789)

            remote-ejb-to-quarkus-00000:
              description: Remote EJBs are not supported in Quarkus
              incidents:
              - uri: file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
              message: "Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:\n 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path(\"<endpoint>\")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.\n 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.\n 3. For every public method on the EJB being converted, do the following:\n - Annotate the method with `@jakarta.ws.rs.GET`\n - Annotate the method with `@jakarta.ws.rs.Path(\"<endpoint>\")` and give it a proper endpoint path. As a rule of thumb... <snip for readability>"

              lineNumber: 12
              variables:
                file: file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
                kind: Class
                name: Stateless
                package: com.redhat.coolstore.service

              - url: https://jakarta.ee/specifications/restful-ws/
                title: Jakarta RESTful Web Services

  1.  Solved Examples - these are source code diffs that show a LLM how a similar problem was seen in another application the Organization has and how that Organization decided to fix it.

      - We mine data Konveyor has stored from the Application Hub to search for when other applications have fixed the same rule violations and learn how they fixed it and pass that info into the prompt to aid the LLM
      - This ability to leverage how the issue was seen and fixed in the past helps to give the LLM extra context to give a higher quality result.
      - This is an [early prompt we created](https://github.com/konveyor-ecosystem/kai/blob/main/notebooks/jms_to_smallrye_reactive/output/gpt-4-1106-preview/helloworldmdb/custom-ruleset/jms-to-reactive-quarkus-00050/few_shot/template.txt) to help give a feel of this in action and the [result we got back from a LLM](https://github.com/konveyor-ecosystem/kai/blob/main/notebooks/jms_to_smallrye_reactive/output/gpt-4-1106-preview/helloworldmdb/custom-ruleset/jms-to-reactive-quarkus-00050/few_shot/result.txt)

## Pre-Requisites

### Access to a Large Language Model (LLM)

- If you want to run Kai against a LLM you will likely need to configure a LLM API Key to access your service (unless running against a local model)
  - We do provide a means of running Kai against previously cached data from a few models to aid demo flows. This allows you to run through the steps of using previously cached data without requiring access to a LLM. Note, if you do not provide LLM API access then the DEMO_MODE flow will only be able to replay previous cached responses.
    - We call this 'DEMO_MODE', i.e. `DEMO_MODE=true make run-server`
- Note that results vary widely between models.

#### LLM API Keys

- We expect that you have configured the environment variables required for the LLM you are attempting to use.
  - For example:
    - OpenAI service requires: `OPENAI_API_KEY=my-secret-api-key-value`
    - IBM BAM service requires: `GENAI_KEY=my-secret-api-key-value`

#### IBM BAM Service

- The development team has been using the IBM BAM service to aid development and testing:

      IBM Big AI Model (BAM) laboratory is where IBM Research designs, builds, and iterates on what’s next in foundation models. Our goal is to help accelerate the transition from research to product. Come experiment with us.

  - Login: https://bam.res.ibm.com/
    - In order to use this service an individual needs to obtain a w3id from IBM. The kai development team is unable to help obtaining this access.
  - Related client tooling:

    - https://github.com/IBM/ibm-generative-ai
    - LangChain integration: https://ibm.github.io/ibm-generative-ai/v2.2.0/rst_source/examples.extensions.langchain.html#examples-extensions-langchain

  - Obtain your API key from IBM BAM:

    - To access via an API you can look at ‘Documentation’ after logging into https://bam.res.ibm.com/
      - You will see a field embedded in the 'Documentation' section where you can generate/obtain an API Key.

  - Ensure you have `GENAI_KEY=my-secret-api-key-value` defined in your shell

#### OpenAI Service

- If you have a valid API Key for OpenAI you may use this with Kai.
- Ensure you have `OPENAI_API_KEY=my-secret-api-key-value` defined in your shell

##### Selecting a Model

We offer configuration choices of several models via [config.toml](/kai/config.toml) which line up to choices we know about from [kai/model_provider.py](https://github.com/konveyor-ecosystem/kai/blob/main/kai/model_provider.py).

To change which llm you are targeting, open `config.toml` and change the `[models]` section to one of the following:

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**IBM served granite**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatIBMGenAI"

  [models.args]
  model_id = "ibm/granite-13b-chat-v2"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**IBM served mistral**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatIBMGenAI"

  [models.args]
  model_id = "mistralai/mixtral-8x7b-instruct-v01"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**IBM served codellama**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatIBMGenAI"

  [models.args]
  model_id = "meta-llama/llama-2-13b-chat"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**IBM served llama3**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
  # Note:  llama3 complains if we use more than 2048 tokens
  # See:  https://github.com/konveyor-ecosystem/kai/issues/172
[models]
  provider = "ChatIBMGenAI"

  [models.args]
  model_id = "meta-llama/llama-3-70b-instruct"
  parameters.max_new_tokens = 2048
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**Ollama**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatOllama"

  [models.args]
  model = "mistral"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**OpenAI GPT 4**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatOpenAI"

  [models.args]
  model = "gpt-4"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

<!-- trunk-ignore-begin(markdownlint/MD036) -->

**OpenAI GPT 3.5**

<!-- trunk-ignore-end(markdownlint/MD036) -->

<!-- trunk-ignore-begin(markdownlint/MD046) -->

```toml
[models]
  provider = "ChatOpenAI"

  [models.args]
  model = "gpt-3.5-turbo"
```

<!-- trunk-ignore-end(markdownlint/MD046) -->

Kai will also work with [OpenAI API Compatible alternatives](docs/OpenAI-API-Compatible-Alternatives.md).

## Setup

Running Kai's backend involves running 2 processes:

- Postgres instance which we deliver via container
- Backend REST API server

### Steps

1. Clone Repo and Ensure you have the virtual environment setup
   1. `git clone https://github.com/konveyor-ecosystem/kai.git`
   1. `cd kai`
   1. `python3 -m venv env`
      - We've tested this with Python 3.11 and 3.12
   1. `source env/bin/activate`
   1. `pip install -r ./requirements.txt`
   1. `pip install -e .`
1. Run the Postgres DB via podman
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-postgres`
1. Run the Kai server in background
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-server`
      - If you want to run with cached LLM responses run with `DEMO_MODE=true`
        - Replace the above command and instead run: `DEMO_MODE=true make run-server`
        - The `DEMO_MODE` option will cache responses and play them back on subsequent runs.
      - If you want to run with debug information set the environment variable `LOG_LEVEL=debug`
        - Example: `LOG_LEVEL=debug make run-server`
1. Load data into the database
   1. `source env/bin/activate`
   1. Fetch sample apps: `pushd samples; ./fetch_apps.py; popd`
   1. `make load-data`
      - This will complete in ~1-2 minutes

## How to use Kai?

### Client Usage

- There are a few ways to use Kai
  - IDE usage: See: [Install the Kai VSCode Plugin](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md)
  - CLI that scripts usage to the API
    1. We have a script: [example/run_demo.py](example/run_demo.py) that will look at Kantra analysis of the [coolstore](https://github.com/konveyor-ecosystem/coolstore) application and will issue a series of requests to Kai to generate a Fix and then store those fixes back to the application.
    1. See [example/README.md](example/README.md) to learn more how to run this

## Demo

### Demo Overview

- We have a demo that will walk through the migration of a sample application written for EAP with Java EE and bring it to Quarkus.
- Sample Application
  - https://github.com/konveyor-ecosystem/coolstore
    - We will use the `main` branch which has the Java EE version.
    - We have found [these issues](https://github.com/jmle/kai-examples/blob/main/coolstore-examples/examples.md) in the `main` branch which need to be addressed before we move to Quarkus:
      - This information was obtained by running [Kantra](https://github.com/konveyor/kantra) (Konveyor's static code analyzer) with these [custom-rules](https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules)
        - Full output from [Kantra](https://github.com/konveyor/kantra) is checked into the git repo here: [example/analysis/coolstore](example/analysis/coolstore)

### What are the general steps of the demo?

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

### Demo Video

![DemoVideo](/images/Kai_April_26c.gif)

- See [Generative AI Applied to Application Modernization with Konveyor AI](https://www.youtube.com/watch?v=aE8qNY2m4v4) (~15 minute demo with voice)

### Guided walk-through using Kai

- See [docs/demo.md](docs/demo.md) for a guided walkthrough of how to use Kai to aid in a Java EE to Quarkus migration

## Notes on `DEMO_MODE` and cached responses

The kai server will always cache responses in the `kai/data/vcr/<application_name>/<model>` directory. In non-demo mode, these responses will be overwritten whenever a new request is made.
When the server is run with `DEMO_MODE=true`, these responses will be played back. The request will be matched on everything except for authorization headers, cookies, content-length and request body.

### `DEMO_MODE` Cached Responses

- We do not actively maintain cached responses for all models/requests.
- You may look at: [kai/data/vcr/coolstore](kai/data/vcr/coolstore/) to see a list of what models have cached responses.
  - In general when we cache responses we are running: [example/run_demo.py](example/run_demo.py) and saving those responses.
    - This corresponds to a 'KAI Fix All' being run per file in Analysis.
- When running from IDE and attempting to use cached response, we likely only have cached responses for 'Fix All', and we do not have cached responses for individual issues in a file.

### `DEMO_MODE` Updating Cached Responses

There are two ways to record new responses:

1. Run the requests while the server is not in `DEMO_MODE`
1. Delete the specific existing cached response (under `kai/data/vcr/<application_name>/<model>/<source-file-path-with-slashes-replaced-with-dashes.java.yaml>`), then rerun. When a cached response does
   not exist, a new one will be recorded and played back on subsequent runs.

## Contributors

- Below information is only needed for those who are looking to contribute, run e2e tests, etc.

### Updating requirements.txt

- If you are a developer working on Kai and you are updating requirements.txt, you will need to do some manual changes beyond just a `pip freeze &> ./requirements.txt`, we have a few directives that address differences in 'darwin' systems that need to be preserved. These need to be added manually after a 'freeze' as the freeze command is not aware of what exists in requirements.txt. Please consult the diff of changes you are making now from prior version and note the extra directions for `python_version` and or `sys_platform`

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

### Linting

1. Install trunk via: https://docs.trunk.io/check#install-the-cli
1. Run the linters: `trunk check`
1. Format code: `trunk fmt`

### Testing

#### How to run regression tests

1. Install the prerequisites in Setup and activate the python virtual environment
2. Ensure you've checked out the source code for sample applications: Run: [./samples/fetch_sample_apps.sh](./samples/fetch_sample_apps.sh)
3. Run: [./run_tests.sh](./run_tests.sh)

## Prototype

This repository represents a prototype implementation as the team explores the solution space. The intent is for this work to remain in the konveyor-ecosystem as the team builds knowledge in the domain and experiments with solutions. As the approach matures we will integrate this properly into Konveyor and seek to promote to github.com/konveyor organization.

## Code of Conduct

Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
