# Konveyor AI (Kai) Roadmap

This document is a roadmap for Konveyor AI (Kai). The roadmap is organized by themes of functionality, each focusing on a specific aspect of the project's development.

Roadmap Ouline:

- [Guiding Principles](#guiding-principles)
- [Themes](#themes)
- [Milestones](#milestones)
- [Future Areas to Consider](#future-areas-to-consider)

**What is the purpose of Konveyor AI?**
Kai intends to improve the economics of re-platforming and refactoring applications to Kubernetes and cloud-native technologies via use of Generative AI leveraging data in Konveyor.

**Maturity - Early Development**
_Kai is in early stages of development and is NOT suitable for production usage at this time._

- Please see [docs/Evaluation_Builds.md](docs/Evaluation_Builds.md) to learn more about early access preview builds.
- Contributions are encouraged and most welcome, for more information see [CONTRIBUTING.md](CONTRIBUTING.md)

## Guiding Principles

**Model agnostic - Bring Your Own Model**
We recognize the rapid pace of evolving Large Language Models (LLM), for that reason the team is approaching implementation tasks in a manner to allow swappable artifacts to aid the adoption of various LLM providers.

- An important aspect of the project's mission is to empower the end user to experiment with various LLMs and ultimately choose which model they want to leverage.

**Embrace a Learning Mindset for Experiments to Solidify Knowledge**
Konveyor AI is committed to a learning mindset in regard to feature development. We recognize that not all features will have an immediate beneficial impact, and the nature of this domain involves making small bets to explore different approaches. The team will focus on experimentation to understand what works and what doesn't, thereby improving the quality of results.

The development team contributing to Konveyor AI acknowledges that this is a rapidly evolving field. To succeed, we must invest in experiments to solidify our understanding, identify effective strategies, and share knowledge from this learning with the community.

Our approach includes:

- Utilizing Jupyter notebooks to prototype and share new feature experiments, allowing others to explore the methodologies.
- Including both successful and failed experiments in our project resources to share knowledge and learnings.
- Implementing feature gates to enable or disable experimental features as needed.
- Providing configuration options to adjust algorithmic choices and parameters as well as prompt templating to allow rapid prototyping.

## Themes

The below themes are areas of improvement the team has identified for future work.

- [Use Konveyor Data to Improve Generated Results](#use-konveyor-data-to-improve-generated-results)
- [Konveyor Integration](#konveyor-integration)
- [Repository Level Understanding and Code Generation](#repository-level-code-generation)
- [IDE Integrations](#ide-integrations)
- [User Experience Improvements](#user-experience-improvements)
- [External Tool Integrations](#external-tool-integrations)
- [Evaluation Tools to Benchmark Results](#external-tool-integrations)
- [Scenario Creation to Showcase Capabilities](#scenario-creation-to-showcase-capabilities)
- [InstructLab Integrations to Aid Fine Tuning](#instructlab-integrations-to-aid-fine-tuning)

### Use Konveyor Data to improve generated results

- Improve the Retrieval Augmented Generation (RAG) approach which uses application modernization data inside of Konveyor to aid shaping code generations for better alignment of how an organization has solved that given problem in the past.
- Measure confidence of generated results.
  - Track the acceptance | rejection rate of generated results vs known analysis incidents to give end user a sense of confidence for a given generation.

### Konveyor Integration

- Sync Konveyor's application modernization data with Kai's database
- Deploy Kai from Konveyor's Operator
- Integrate Kai so it is accessible via Konveyor's endpoint and integrated with Konveyor's Auth

### Repository Level Code Generation

- Techniques to overcome limited context windows with LLM requests to faciliate a broader repository level understanding of code flows and modifications

### IDE Integrations

- IDE Integrations
  - VSCode (1st IDE to Integrate)
  - Intelli-J (2nd IDE to Integrate)
  - Eclipse (3rd IDE to Integrate)
- Real-time updates of static code analysis
  - Integrate [analyzer-lsp](https://github.com/konveyor/analyzer-lsp) into the IDE with the ability to perform updates of static code analysis information as each file is modified.
- Improve UX of IDE Plugin
  - For VSCode IDE Plugin move the Kai specifics out of a separate 'Kai' view into the main 'Explorer' view

### User Experience Improvements

- Developer Workflow Experience
  - Establish a incremental migration experience to aid the scenario of translating an application from one technology to another in a manageable/incremental manner.
- Create a ChatBot interface to provide an additional method of interaction via a conversational experience

### External Tool integrations

- Integrate external tools such as linters, compilers, execution of tests in an agent workflow to iterate and improve on a generated code snippet.

### Evaluation Tools to Benchmark Results

- Establish a means of evaluating the quality of generated results to aid learning from experiments

### Scenario Creation to Showcase Capabilities

- In order to show the capabilities of Kai artifacts are required such as multiple sample applications and [analysis rules](https://github.com/konveyor/rulesets/tree/main/default/generated). For example, Kai has begun with a scenario of showing Java EE to Quarkus, yet other technologies are possible dependent on the availability of sample applications and analysis rules.

### InstructLab Integrations to aid Fine Tuning

[InstructLab](https://github.com/instructlab) is an open-source community focused on aiding fine-tuning of LLMs

- While fine-tuning of a LLM is out of scope for Kai itself and is NOT required, we recognize that the community will benefit from leveraging data inside of Konveyor and Kai to aid fine tuning code models for improved modernization activities.

## Milestones

_Kai releases will be considered independent of Konveyor releases for the initial period of functionality development. We expect to see Kai releases tied to Konveyor releases in 2025._

- [**August 2024**: Prototype](#2024---august-prototype)
- [**October 2024**: Kai v0.1.0 Release](#october-2024-kai-v010-release)
- [**December 2024**: Kai v0.2.0 Release](#december-2024-kai-v020-release)
- [**February 2025**: Kai v0.3.0 Release](#february-2025-kai-v030-release)

## 2024 - August: Prototype

### Summary

_The prototype is able to sync data from Konveyor or use existing sample data to aid a scenario of Java EE to Quarkus migration. A minimal workflow is provided to aid early evalations by interested contributors_

- Workflow is focused at level of a single file, i.e. lacks awareness of full context of repository
- Minimal IDE integration in VSCode, workflow is functional to show a happy path
- IDE integrates [Kantra](https://github.com/konveyor/kantra) to find modernization issues via static analysis
- Forms a prompt to request an updated code fix via a LLM.
- Augments the prompt with 2 sources of extra data
  - Analysis Hints from Kantra
  - [Optional] information of how similar problems were solved in past.

### Key Deliverables

- _Konveyor Integration_
  - Add the ability to ingest data from Konveyor Hub, able to pull data from Konveyor 0.5.0
  - A separate process will run that continuously syncs data from Konveyor into Kai
- _Use Konveyor data to improve generated results_
  - Analysis Hints - Contextual information associated with [Analysis Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) that provide information of a specific incident
  - Prior patterns of solved examples similar to a given incident
    - Introduce 'Solved Incident Store' component which will allow Kai to see how an organization has solved a similar analysis problem in the past. The component will work with a LLM to summarize the key pieces of how a similar solution was solved by the organization in the past and include that summarization to help the LLM steer the generated solution closer to a desired result
- _IDE Integration_
  - VSCode IDE Integration: Identification of existing modernization issues via static code analyis from [Kantra](https://github.com/konveyor/kantra) in VSCode IDE
    - **Limitation**: Analysis will NOT automatically update. Kantra analysis needs to be manually re-run to refresh analysis information.
    - Workflow is the minimal needed to show happy-path, more work is needed before this is ready for the end user

## October 2024: Kai v0.1.0 Release

### Summary

_The v0.1.0 release is focused on improving the user experience from the IDE by providing quicker analysis updates as each file is saved. Additionally, Kai will be integrated into Konveyor, with the ability to be deployed from the Konveyor Operator._

### Key Deliverables

- _Konveyor Integration_
  - Kai is deployed within Konveyor from the Konveyor Operator, tentative Konveyor 0.6.0 target
  - IDE is able to communicate with the remote Kai service which is integrated behind Konveyor's auth
- _IDE Integration_
  - VSCode IDE Integration: Real-time updates of analysis information via replacement of [Kantra](https://github.com/konveyor/kantra) with [analyzer-lsp](https://github.com/konveyor/analyzer-lsp)
    - Benefit: Analysis information will be updated automatically as a file is modified.
- _Evaluation Tools to Benchmark Results_
  - Establish a benchmark tool to aid scoring generated results against test data. This is first step to aid a metric driven approach to measure experiments to guide result improvements.

## December 2024: Kai v0.2.0 Release

### Summary

_The v0.2.0 release is focused on improving the quality of generated results by establishing an agent workflow that incorporates external tools to iterate on improving a code snippet with a LLM._

### Key Deliverables

- _External Tool integrations_
  - Agent Workflow leveraging tools and iterate with LLM to address errors and improve results

## February 2025: Kai v0.3.0 Release

### Summary

_The v0.3.0 release is focused on teaching Kai how to understand repurcussions of changes that cascade throughout a repository._

### Key Deliverables

- _Repository Level Code Generation_
  - Agent workflow to develop a plan for how to address edits that span throughout the repository, i.e. code changes that have an impact beyond the scope of a single file.

## Future Areas to Consider

The below are additional areas of interest for Konveyor AI, yet are not inline for immediate work. We consider the below as inspirational areas to consider but are not actively working.

- Code Explanation/Summarization
- Test Generation
- Generation of OpenRewrite Recipes from Analysis Rules
- Generate analysis rules based on documentation and changelogs
