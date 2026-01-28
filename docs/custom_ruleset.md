# Custom Rules Integration

When you have written custom rules and would like to add them to your issues to be solved by Kai's reactive code plan.  
You will need to take a few steps to make this work.

## Steps to Add Custom Rulesets

### Stop the Running Server

If the server is running you will need to stop it.  
To see if the server is running, open the `Konveyor Analysis View`

![image](images/custom_rules/running_server.png)

You will need to click the `Stop` button here if the server is running.

Once the server is stopped, you can move on to the next step.

### Adding Custom Rulesets

To add your custom rulesets, you will need to have a directory containing a `ruleset.yaml` file, and the subsequent rule files. You can find examples of that [here](https://github.com/konveyor/rulesets/tree/main/default/generated) as well as docs around [rules and rulesets](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md).

> [!IMPORTANT]
> For the next example, we will assume a ruleset at `/Users/user/rulesets/custom-ruleset`. You will need to change this to point to your ruleset directory.

First you will need to open up the `Profile Manager` in the `Get Ready to Analyze` view:

![image](images/custom_rules/search_custom_rules.png)

Then you can click `Select Custom Rules`, and select the custom rules in your path. We will use the example path.

![image](images/custom_rules/add_custom_ruleset.png)

### Running Analysis

Now you can return to the `Konveyor Aanlysis View` page and start the server.

![image](images/custom_rules/running_server.png)

Click `Run Analysis`, and your custom ruleset will be used.

> [!WARNING]
> You will need to make sure that the rules or rulesets have a target or source label that is selected. If the ruleset does not match a selected target or source, it will be filtered out and skipped.

## Creating Rules and Rulesets

### Determing rules

To create custom rules, you need to know of a change that must happen to complete a migration. This could be because of a framework or library that you are using (either an internal one or external/open source one).  
For this section, I am going to create a rule and ruleset for an open source framework, but the process should be similar for any custom rule.

To find a place for a rule, we are going to look at the release notes of the Quarkus framework. If we see the [section](https://github.com/quarkusio/quarkus/wiki/Migration-Guide-3.18#kubernetes-client-fabric8) here. If we follow this to the migration guide for this dependency, we can see this [section](https://github.com/fabric8io/kubernetes-client/blob/main/doc/MIGRATION-v7.md#kubernetes-model-artifact-removed-).

> The Maven artifact `io.fabric8:kubernetes-model` has been removed from the project, and is no longer published.
> This artifact was an aggregator of some of the Kubernetes model artifacts, and had no specific purpose. `io.fabric8:kubernetes-client-api` or `io.fabric8:kubernetes-openshift-uberjar` artifacts should be used instead.

We will need to make sure that if the dependency `io.fabric8:kubernetes-model` is being used, that we alert the user, and tell them what they should be using instead.

### Creating the custom rule

Now we need to see how a rule is configured.

- The [rules](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md#rule-metadata) documentation states that we will need to set up the metadata first. In this case, we will use the below yaml for this.

```yaml
- ruleID: "fabric8-remove-kubernetes-model-00001"
  labels:
    - "konveyor.io/target=quarkus"
  effort: 1
  category: mandatory
```

- Next, we will add a description. This description will describe what issue entails. I think the migration docs do a good job of this, so we can use what is mentioned there:

```yaml
description: |
  The Maven artifact io.fabric8:kubernetes-model has been removed from the project and is no longer published.

  This artifact was just an aggregator of some of the Kubernetes model artifacts and had no specific purpose. It is no longer published, the io.fabric8:kubernetes-client-api or io.fabric8:kubernetes-openshift-uberjar artifacts should be used instead."
```

- Next, we need to decide what [Action](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md#rule-actions) to take. It is worth noting that for Kai, the only action that will be used is `message`.
  The message is used by the LLM to generate a fix for the issue.

> [!WARNING]
> If you use only the tag action, or if you don't set effort, then the rule's violations will not be used by Kai.

> [!NOTE]
> This process may require some iteration to determine the optimal message for generating the fix for your issue and model.

```yaml
  message: |
  	The Maven artifact io.fabric8:kubernetes-model has been removed from the project and is no longer published.

  	This artifact was just an aggregator of some of the Kubernetes model artifacts and had no specific purpose. It is no longer published, the io.fabric8:kubernetes-client-api or io.fabric8:kubernetes-openshift-uberjar artifacts should be used instead."
```

- Now that we have all the information captured in our rule for using it in Kai, we need to add when this should be triggered. This is the `when` clause for a rule. We call these [conditions](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md#rule-conditions). Different providers will support different conditions. Today in Kai, we only have two providers, the `java` and `builtin` providers.
  - For this issue, we are looking at dependencies, and so we will choose to use the `java.dependency` [capability](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md#provider-condition).

```yaml
  when:
  	java.dependency:
  		name: io.fabric8.kubernetes-model
```

- Save this file in a directory for this ruleset, and create a `ruleset.yaml` in the same directory.
  - The [ruleset.yaml](https://github.com/konveyor/analyzer-lsp/blob/main/docs/rules.md#ruleset) is a special file that groups these rules together to help make their management easier.
    We will use this ruleset for this rule:

```yaml
name: quarkus-3-18
description: These rules are created from the 3.18 migration guide.
labels:
  - "konveyor.io/target=quarkus"
```

This custom ruleset should now be usable for an analysis in Kai.
