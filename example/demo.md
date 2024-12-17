# Kai Demo

Konveyor AI (kai) is Konveyor's approach to easing modernization of application
source code to a new target by leveraging LLMs with guidance from static code
analysis augmented with data in Konveyor that helps to learn how an Organization
solved a similar problem in the past.

- [Kai Demo](#kai-demo)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Step 1: Setup](#step-1-setup)
    - [Running Kai with IBM-served Llama 3](#running-kai-with-ibm-served-llama-3)
    - [Running Kai with Amazon Bedrock-served Llama 3](#running-kai-with-amazon-bedrock-served-llama-3)
    - [Running Kai with GPT-3.5-Turbo](#running-kai-with-gpt-35-turbo)
    - [Running Kai with Cached Responses Only (demo mode)](#running-kai-with-cached-responses-only-demo-mode)
  - [Step 2: Clone the coolstore app](#step-2-clone-the-coolstore-app)
  - [Step 3: Run Kai](#step-3-run-automated-usage-of-kai)
  - [Conclusion](#conclusion)

## Overview

In this demo, we will showcase the capabilities of Konveyor AI (Kai) in
facilitating the modernization of application source code to a new target. We
will illustrate how Kai can handle various levels of migration complexity,
ranging from simple import swaps to more involved changes such as modifying
scope from CDI bean requirements. Additionally, we will look into migration
scenarios that involves EJB Remote and Message Driven Bean(MBD) changes

We will focus on migrating a partially migrated [JavaEE Coolstore
application](https://github.com/konveyor-ecosystem/coolstore.git) to Quarkus, a
task that involves not only technical translation but also considerations for
deployment to Kubernetes. By the end of this demo, you will understand how
Konveyor AI (Kai) can assist and expedite the modernization process.

This demo will focus primarly in driving Kai's RPC server via helper scripts.
This guide will not cover the IDE integration.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/downloads)
- [GenAI credentials](../docs/llm_selection.md#ibm-bam-service)
- [Maven](https://maven.apache.org/install.html)
- Quarkus 3.10
- Java 17

## Step 1: Setup

[You can configure Kai in multiple ways](../docs/contrib/configuration.md). The best
way to configure Kai is with a `config.toml` file. For this walkthrough, we
will create `example/config.toml` with a very minimal configuration to get
started.

When not running in demo mode, you will need to select an LLM model to use with
Kai. Here are some examples of how to configure Kai to use different models.
For more options, see [llm_selection.md](../docs/llm_selection.md).


> [!IMPORTANT]
>
> The demo assumes you are using IBM-served Llama 3. If you are using a different
> model, the responses you get back may be different.

### Running Kai with IBM-served Llama 3

<!-- Begin copy from llm_selection.md#ibm-bam-service -->

> [!WARNING]  
> In order to use this service an individual needs to obtain a w3id
> from IBM. The kai development team is unable to help obtaining this access.

1. Login to https://bam.res.ibm.com/.
2. To access via an API you can look at ‘Documentation’ after logging into
   https://bam.res.ibm.com/. You will see a field embedded in the
   'Documentation' section where you can generate/obtain an API Key.
3. Ensure you have exported the key via `export
GENAI_KEY=my-secret-api-key-value`.

<!-- End copy from llm_selection.md#ibm-bam-service -->

Next, paste the following into your `example/config.toml` file:

```toml
[models]
provider = "ChatIBMGenAI"

[models.args]
model_id = "meta-llama/llama-3-70b-instruct"
parameters.max_new_tokens = 2048
```

### Running Kai with Amazon Bedrock-served Llama 3

1. Obtain your AWS API key from Amazon Bedrock.
2. Export your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and
   `AWS_DEFAULT_REGION` environment variables.

Next, paste the following into your `build/config.toml` file:

```toml
[models]
provider = "ChatBedrock"

  [models.args]
  model_id = "meta.llama3-70b-instruct-v1:0"
```

Finally, run the backend with `podman compose up`.

### Running Kai with GPT-3.5-Turbo

<!-- Begin copy from llm_selection.md#openai-service -->

1. Follow the directions from OpenAI
   [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key).
2. Ensure you have exported the key via `export
OPENAI_API_KEY=my-secret-api-key-value`

<!-- End copy from llm_selection.md#openai-service -->

Next, paste the following into your `example/config.toml` file:

```toml
[models]
provider = "ChatOpenAI"

[models.args]
model = "gpt-3.5-turbo"
```

### Running Kai with Cached Responses Only (demo mode)

By default, this example demo script will run Kai in demo mode, which uses
cached responses.  This is helpful if you don't have access to an LLM.
Additionally, the responses are determinstic rather than slight changes based
oan LLM response.

### Install Kai
Download Kai server and analyzer binaries for your machine and place them in
our example directory. First, download the zip file for your OS
[here](https://github.com/konveyor/kai/releases/tag/v0.0.1). Unzip the
directory and copy the binaries to `example/analysis`.
```
$ cp ~/Downloads/kai-rpc-server.linux-x86_64/kai-rpc-server example/analysis/
$ cp ~/Downloads/kai-rpc-server.linux-x86_64/kai-analyzer-rpc example/analysis/
```

### Setup analysis dependencies

#### Start JDTLS in docker
The simplest way to start JDTLS is to use docker:
```
$ docker run -d --name=bundle quay.io/konveyor/jdtls-server-base:latest
```

#### Copy dependencies

Copy the JDTLS binary and other needed files out of the container:
```
$ docker cp bundle:/usr/local/etc/maven.default.index ./example/analysis
$ docker cp bundle:/jdtls ./example/analysis
$ docker cp bundle:/jdtls/java-analyzer-bundle/java-analyzer-bundle.core/target/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar ./example/analysis/bundle.jar
$ docker cp bundle:/usr/local/etc/maven.default.index ./example/analysis 
```

Now `example/analysis` contains all of the needed dependencies to run Kai

## Step 2: Clone the coolstore app

Let's clone the Coolstore application, which we will be used demo the migration
process to Quarkus.

Clone the Coolstore demo from its repository:

```sh
$ cd example/
$ git clone https://github.com/konveyor-ecosystem/coolstore.git
```

## Step 3: Run Automated Usage of Kai

We will use a helper script that will perform an analysis of the Coolstore
application using the following migration targets to identify potential areas
for improvement:

<!-- - containerization -->

- jakarta-ee
- jakarta-ee8
- jakarta-ee9
- quarkus

To run Kai, we can use `run_demo.py` which will start up the Kai RPC server and run the limited agentic workflow to migrate the coolstore application to quarkus.

<!-- TODO: Update this -->