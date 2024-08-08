# Tracing

The Kai server is able to capture LLM tracing information and write to disk to aid debugging.

Kai's tracing is currently simple, we will write to disk but are not integrated with any LLM observability tools.

Tracing will gather information and write to various files under the 'logs/trace' directory.

Tracing can be enabled or disabled.
It is enabled via:

- Environment variable: `TRACE=true`
- kai/config.toml

      trace_enabled = true

Example of information captured with tracing:

- Prompt
- LLM Result
- Request Parameters
- Exceptions
- Duration of each request

Tracing info is written to a directory hierarchy structure of:

    logs/trace/{model}/{app_name}/{src_file_path}/{batch_mode}/{timestamp_of_request}/{incident_batch_number}/{retry_attempt}

Example of hierarchy:

      └── trace
          └── gpt-3.5-turbo << MODEL ID>>
              └── coolstore << APP Name >>
                  ├── pom.xml << Source File Path >>
                  │   └── single_group << Incident Batch Mode >>
                  │       └── 1719673609.8266618 << Start of Request Time Stamp >>
                  │           ├── 1 << Incident Batch Number >>
                  │           │   ├── 0 << Retry Attempt  >>
                  │           │   │   └── llm_result << Contains the response from the LLM prior to us parsing >>
                  │           │   ├── prompt << The formatted prompt prior to sending to LLM >>
                  │           │   └── prompt_vars.json << The prompt variables which are injected into the prompt template >>
                  │           ├── params.json << Request parameters >>
                  │           └── timing << Duration of a Successful Request >>
                  └── src
                      └── main
                          ├── java
                          │   └── com
                          │       └── redhat
                          │           └── coolstore
                          │               ├── model
                          │               │   ├── InventoryEntity.java
                          │               │   │   └── single_group
                          │               │   │       └── 1719673609.827135
                          │               │   │           ├── 1
                          │               │   │           │   ├── 0
                          │               │   │           │   │   └── llm_result
                          │               │   │           │   ├── prompt
                          │               │   │           │   └── prompt_vars.json
                          │               │   │           ├── params.json
                          │               │   │           └── timing
                          │               │   ├── Order.java
                          │               │   │   └── single_group
                          │               │   │       └── 1719673609.826999
                          │               │   │           ├── 1
                          │               │   │           │   ├── 0
                          │               │   │           │   │   └── llm_result
                          │               │   │           │   ├── prompt
                          │               │   │           │   └── prompt_vars.json
                          │               │   │           ├── params.json
                          │               │   │           └── timing
