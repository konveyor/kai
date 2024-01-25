#!/bin/bash

./run_cli.py generate ./samples/analysis_reports/eap-coolstore-monolith/output.yaml \
    ./samples/sample_repos/eap-coolstore-monolith main quarkus-migration \
    ./samples/generated_output/eap-coolstore-monolith \
    -m 'gpt-3.5-turbo-16k' \
    -r 'quarkus/springboot' \
    -v 'cdi-to-quarkus-00040' -v 'cdi-to-quarkus-00050'

## Models
# gpt-3.5-turbo-16k
# gpt-4-1106-preview
