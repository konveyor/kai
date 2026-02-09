# Overview

This document contains background information to help understand the technical approach Konveyor AI (Kai) is following.

- [Overview](#overview)
  - [Approach](#approach)
    - [What happens technically to make this work?](#what-happens-technically-to-make-this-work)
  - [Further Reading](#further-reading)

## Approach

Kai implements a [Retrieval Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) approach that leverages data from Konveyor to help generate code suggestions to aid migrating legacy code bases to a different technology. The intent of this RAG approach is to shape the code suggestions to be similar to how an organization has solved problems in the past, without additional fine-tuning of the model.

The approach begins with using static code analysis via the [Kantra](https://github.com/konveyor/kantra) tool to find areas in the source code that need attention. 'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

This approach does _not_ require fine-tuning of LLMs, we augment a LLMs knowledge via the prompt, by leveraging external data from inside of Konveyor and from Analysis Rules to aid the LLM in constructing better results.

For example, [analyzer-lsp Rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md) such as these ([Java EE to Quarkus rulesets](https://github.com/konveyor/rulesets/tree/main/default/generated/quarkus)) are leveraged to aid guiding a LLM to update a legacy Java EE application to Quarkus

Note: For purposes of this initial prototype we are using an example of Java EE to Quarkus. That is an arbitrary choice to show viability of this approach. The code and the approach will work on other targets that Konveyor has rules for.

### What happens technically to make this work?

- [Konveyor](konveyor.io) contains information related to an Organization's Application Portfolio, a view into all of the applications an Organization is managing. This view includes a history of analysis information over time, access to each applications source repositories, and metadata that tracks work in-progress/completed in regard to each application being migrated to a given technology.

- When 'Konveyor AI' wants to fix a specific issue in a given application, it will mine data in Konveyor to extract 2 sources of information to inject into a given LLM prompt.

  1.  Static Code Analysis

      - We pinpoint where to begin work by leveraging static code analysis to guide us
      - The static code analysis is informed via a collection of crowd sourced knowledge contained in our [rulesets](https://github.com/konveyor/rulesets/tree/main) plus augmented via custom-rules
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
      - Early prototypes used prompt templates and few-shot examples to demonstrate this capability in action.

## Further Reading

For a deeper technical look at Kai please see the konveyor.io blog post from 2024 May 07: [Kai - Generative AI Applied to Application Modernization](https://www.konveyor.io/blog/kai-deep-dive-2024/)
