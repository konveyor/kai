# Large Language Model (LLM) configuration

## LLM API Keys

- We expect that you have configured the environment variables required for the LLM you are attempting to use.
  - For example:
    - OpenAI service requires: `OPENAI_API_KEY=my-secret-api-key-value`
    - IBM BAM service requires: `GENAI_KEY=my-secret-api-key-value`

## IBM BAM Service

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

## OpenAI Service

- If you have a valid API Key for OpenAI you may use this with Kai.
- Ensure you have `OPENAI_API_KEY=my-secret-api-key-value` defined in your shell

## Selecting a Model

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

Kai will also work with [OpenAI API Compatible alternatives](/docs/OpenAI-API-Compatible-Alternatives.md).
