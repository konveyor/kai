# Konveyor AI (kai)
Konveyor AI (kai) is Konveyor's approach to easing modernization of application source code to a new target by leveraging LLMs with guidance from static code analysis.

Pronounciation of 'kai': https://www.howtopronounce.com/kai

### Approach
Our approach is to use static code analysis to find the areas in source code that need to be transformed.  'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

This approach does _not_ require fine-tuning of LLMs, we augment a LLMs knowledge via the prompt, similar to approaches with RAG by leveraging external data from inside of Konveyor and from Analysis Rules to aid the LLM in constructing better results.

For example, [analyzer-lsp Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) such as these ([Java EE to Quarkus rulesets](https://github.com/konveyor/rulesets/tree/main/default/generated/quarkus)) are leveraged to aid guiding a LLM to update a legacy Java EE application to Quarkus.

## Getting Started

### Setup
1. `python -m venv env`
2. `source env/bin/activate`
3. `pip install -r ./requirements.txtpip install -r ./requirements.txt`
4. Install [podman](https://podman.io/) so you can run [Kantra](https://github.com/konveyor/kantra) for static code analysis

### Run an analysis of a sample app (example for MacOS)
1. `cd data`
2. `./fetch.sh` # this will git clone some sample source code apps
3. `./darwin_restart_podman_machine.sh` # setups the podman VM on MacOS so it will mount the host filesystem into the VM
4. `./darwin_get_latest_kantra_cli.sh` # fetches 'kantra' our analyzer tool
5. `./analyzer_coolstuff.sh` # Analyzes 'coolstuff-javaee' directory and writes an analysis output to [example_reports/coolstuff-javaee/output.yaml](/data/example_reports/coolstuff-javaee/output.yaml)
    * Follow that example to analyze other sample applications

## Testing
### How to run regression tests
T.B.D.

## Prototype
This repository represents a prototype implementation as the team explores the solution space.  The intent is for this work to remain in the konveyor-ecosystem as the team builds knowledge in the domain and experiments with solutions.  As the approach matures we will integrate this properly into Konveyor and seek to promote to github.com/konveyor organization.

## Code of Conduct
Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
