# Konveyor AI (kai)

Konveyor AI (kai) is Konveyor's approach to easing modernization of application source code to a new target by leveraging LLMs with guidance from static code analysis augmented with data in Konveyor that helps to learn how an Organization solved a similar problem in the past.

Pronounciation of 'kai': https://www.howtopronounce.com/kai

### Approach

Our approach is to use static code analysis to find the areas in source code that need to be transformed. 'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

This approach does _not_ require fine-tuning of LLMs, we augment a LLMs knowledge via the prompt, similar to approaches with [RAG](https://arxiv.org/abs/2005.11401) by leveraging external data from inside of Konveyor and from Analysis Rules to aid the LLM in constructing better results.

For example, [analyzer-lsp Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) such as these ([Java EE to Quarkus rulesets](https://github.com/konveyor/rulesets/tree/main/default/generated/quarkus)) are leveraged to aid guiding a LLM to update a legacy Java EE application to Quarkus

Note: For purposes of this initial prototype we are using an example of Java EE to Quarkus. That is an arbitrary choice to show viability of this approach. The code and the approach will work on other targets that Konveyor has rules for.

#### What happens technically to make this work?

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

## Demo

### Demo Overview

- We will walk through the migration of a sample application written for EAP with Java EE and bring it to Quarkus.
- Sample Application
  - https://github.com/konveyor-ecosystem/coolstore
    - We will use the `main` branch which has the Java EE version.
    - We have found [these issues](https://github.com/jmle/kai-examples/blob/main/coolstore-examples/examples.md) in the `main` branch which need to be addressed before we move to Quarkus:
      - This information was obtained by running [Kantra](https://github.com/konveyor/kantra) (Konveyor's static code analyzer) with these [custom-rules](https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules)
        - Full output from [Kantra](https://github.com/konveyor/kantra) is checked into the git repo here: [example/analysis/coolstore/markdown/](example/analysis/coolstore/markdown/)

#### What are the general steps of the demo?

1. We launch VSCode with our Kai VS Code extension which is a [modified version of the MTA VSCode Plugin](https://github.com/hhpatel14/rhamt-vscode-extension/tree/kai-2-29)
2. We open a git checkout of a sample application: [coolstore](https://github.com/konveyor-ecosystem/coolstore)
3. We run [Kantra](https://github.com/konveyor/kantra) inside of VSCode to do an analysis of the application to learn what issues are present that need to be addressed before migrating to Quarkus
4. We view the analysis information in VSCode
5. We look at the impacted files and choose what files/issues we want to fix
6. We click 'Generate Fix' in VSCode on a given file/issue and wait ~45 seconds for the Kai backend to generate a fix
7. We view the suggested fix as a 'Diff' in VSCode
8. We accept the generated fix
9. The file in question has now been updated
10. We move onto the next file/issue and repeat

### Demo Pre-requisites

#### LLM API Keys

- Until we fix [this open issue](https://github.com/konveyor-ecosystem/kai/issues/85), you must have an IBM API Key to use kai
- Set the below environment variables in your shell:
  - `GENAI_KEY=my-secret-api-key-value`
- We plan to allow alternative ways of specifiying coordinates in future, tracked via: [Allow model credentials to be stored in an .env file #89](https://github.com/konveyor-ecosystem/kai/issues/89)
  - Once the above issue is fixed we expect to have alternative ways to specifiy model coordinates

##### IBM GenAI

- We are using:

      IBM Big AI Model (BAM) laboratory is where IBM Research designs, builds, and iterates on what’s next in foundation models. Our goal is to help accelerate the transition from research to product. Come experiment with us.

  - Login: https://bam.res.ibm.com/
    - In order to use this service an individual needs to obtain a w3id from IBM. The kai development team is unable to help obtaining this access.
  - Related client tooling:

    - https://github.com/IBM/ibm-generative-ai
    - langchain integration: https://ibm.github.io/ibm-generative-ai/v2.2.0/rst_source/examples.extensions.langchain.html#examples-extensions-langchain

  - Obtain your API key from IBM BAM:
    - To access via an API you can look at ‘Documentation’ after logging into https://bam.res.ibm.com/
      - You will see a field embedded in the 'Documentation' section where you can generate/obtain an API Key.

##### Selecting Other Models

We also support other models. To change which llm you are targeting, open `config.toml` and change the `[models]` section to one of the following:

**IBM served granite**

```toml
provider = "IBMGranite"
args = { model_id = "ibm/granite-13b-chat-v2" }
```

**IBM served mistral**

```toml
provider = "IBMOpenSource"
args = { model_id = "ibm-mistralai/mixtral-8x7b-instruct-v01-q" }
```

**IBM served codellama**

```toml
provider = "IBMOpenSource"
args = { model_id = "meta-llama/llama-2-13b-chat" }
```

**OpenAI GPT 3.5**

```toml
provider = "OpenAI"
args = { model_id = "gpt-4" }
```

**OpenAI GPT 4**

```toml
provider = "OpenAI"
args = { model_id = "gpt-3.5-turbo" }
```

provider = "IBMGranite"

### Demo Steps

#### Backend

- We want to run the 'kai' REST API Server, this will also require a running postgres database and we need to populate that postgress database with a collection of application analysis information from various sample applications. All of the needed data is contained in this repo, we just need to run a command to load it.

1. Clone Repo and Ensure you have the virtual environment setup
   1. `git clone https://github.com/konveyor-ecosystem/kai.git`
   1. `cd kai`
   1. `python3 -m venv env`
      - We've tested this with Python 3.11 and 3.12
   1. `source env/bin/activate`
   1. `pip install -r ./requirements.txt`
1. Run the DB via podman
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-postgres`
1. Run the Kai server in background
   1. Open a new shell tab
   1. `source env/bin/activate`
   1. Let this run in background: `make run-server`
      - Please double check that you have `GENAI_KEY=my-secret-api-key-value` defined in the environment variables prior to running the server.
1. Load data into the database
   1. Can run this in current shell, command will run for a ~1 minute and complete
   1. Ensure you are running within our python virtual env: `source env/bin/activate`
   1. `make load-data`

#### Client Usage

- There are 2 means to use Kai
  - IDE usage, this is the intended demo flow where we:
    1. [Install our VSCode Plugin](https://docs.google.com/document/d/1E2e6hAbrqQNstUuqGHi49F6t2ewYj9iKXPOknrncR6g/edit#heading=h.sgnn4lx17pld)
       - Above is a temporary google doc, we want to clean this up and bring into Markdown in near future.
    1. `git clone https://github.com/konveyor-ecosystem/coolstore`
    1. Open coolstore in VSCode
    1. Run Konveyor Analysis via Kantra inside of the IDE
       - TODO: Instructions forthcoming
- CLI usage (not intended for any demo, but useful for dev team to do test of backend)

  - Run the client: [kai-service/mock-client.py](/kai-service/mock-client.py)

    1.  `source env/bin/activate`
    1.  `cd kai-service`
    1.  `python ./mock-client.py` . (This needs the server to be running above)

            $ python ./mock-client.py
            200
            {"feeling": "OK!", "recv": {"test": "object"}}
            200
            ## Reasoning

            1. In the Java EE code, we are using `@MessageDriven` annotation which is not supported in Quarkus. We need to replace it with a CDI scope annotation like `@ApplicationScoped`.
            2. The `HelloWorldMDB` class is a Message Driven Bean (MDB) that listens to messages on a specified queue and processes them.
            3. The MDB uses the `javax.jms.TextMessage` class to process the messages.
            4. The MDB is activated using the `@ActivationConfigProperty` annotation which specifies the destination type, destination, and acknowledge mode.
            5. To migrate this code to Quarkus, we need to replace the `@MessageDriven` annotation with `@ApplicationScoped` and use CDI for dependency injection.
            6. We also need to update the `onMessage` method to use the `@Incoming` and `Log` annotations provided by Quarkus.

            ## Updated File

            ```java
            // Update the `HelloWorldMDB` class to use CDI and Quarkus annotations
            @ApplicationScoped
            public class HelloWorldMDB {

                @Incoming("CMTQueue")
                public void onMessage(String msg) {
                    Log.info("Received Message: " + msg);
                }
            }
            ```

            This updated file uses the `@ApplicationScoped` annotation to scope the MDB to the application and the `@Incoming` and `Log` annotations to process the messages and log them.
            input...

## Contributors

- Below information is only needed for those who are looking to contribute, run e2e tests, etc.

### Updating requirements.txt

- If you are a developer working on Kai and you are updating requirements.txt, you will need to do some manual changes beyond just a `pip freeze &> ./requirements.txt`, we have a few directives that address differences in 'darwin' systems that need to be preserved. These need to be added manually after a 'freeze' as the freeze command is not aware of what existe in requirements.txt. Please consult the diff of changes you are making now from prior version and note the extra directions for `python_version` and or `sys_platform`

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

1. Install the prereqs in Setup and activate the python virtual environment
2. Ensure you've checked out the source code for sample applications: Run: [./samples/fetch_sample_apps.sh](./samples/fetch_sample_apps.sh)
3. Run: [./run_tests.sh](./run_tests.sh)

## Prototype

This repository represents a prototype implementation as the team explores the solution space. The intent is for this work to remain in the konveyor-ecosystem as the team builds knowledge in the domain and experiments with solutions. As the approach matures we will integrate this properly into Konveyor and seek to promote to github.com/konveyor organization.

## Code of Conduct

Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
