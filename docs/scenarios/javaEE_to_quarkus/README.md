# Modernizing a JavaEE Application to Quarkus Using Konveyor AI

Konveyor AI (kai) is Konveyor's approach to easing modernization of application
source code to a new target by leveraging LLMs with guidance from static code
analysis augmented with data in Konveyor that helps to learn how an Organization
solved a similar problem in the past.

- [JavaEE to Quarkus](#modernizing-a-javaee-application-to-quarkus-using-konveyor-ai)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Step 1: Setup](#step-1-setup)
    - [Install Kai](#installation)
    - [Clone Coolstore app](#get-a-demo-app)
    - [Configure Konveyor](#configure-konveyor-and-start-the-server)
  - [Step 2: Run Analysis](#step-2-run-analysis)
    - [2.1 Change import namespaces](#21-change-import-namespaces)
    - [2.2 Modify Scope from CDI bean requirements](#22-modify-scope-from-cdi-bean-requirements)
    - [2.3 EJB Remote and Message Driven Bean(MDB) changes](#23-ejb-remote)
    - [2.4 JMS to SmallRye](#24-jms-to-smallrye)
  - [Background](#background)
  - [Step 3: Deploy app to Kubernetes](#step-3-deploy-app-to-kubernetes)
  - [Step 4: Debug and File Incidents](#debug-and-file-incidents)
  - [Conclusion](#conclusion)

## Overview

In this demo, we will showcase the capabilities of Konveyor AI (Kai) in
facilitating the modernization of application source code to a new target. We
will illustrate how Kai can handle various levels of migration complexity,
ranging from simple import swaps to more involved changes such as modifying
scope from CDI bean requirements. Additionally, we will look into migration
scenarios that involves EJB Remote and JMS-based Message Driven Bean(MDB) changes.

We will focus on migrating a partially migrated [JavaEE Coolstore
application](https://github.com/konveyor-ecosystem/coolstore.git) to Quarkus, a
task that involves not only technical translation but also considerations for
deployment to Kubernetes. By the end of this demo, you will understand how
Konveyor AI (Kai) can assist and expedite the modernization process.

## Prerequisites

- [VSCode](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [Kubernetes cluster (minikube)](https://minikube.sigs.k8s.io/docs/start/)
- AI credentials
- [Maven](https://maven.apache.org/install.html)
- Java 21

Additionally, you will need to have the Kai IDE plugin installed in VSCode.
Download the latest from
[here](https://github.com/konveyor/editor-extensions/releases).

## Step 1: Setup

### Installation

Follow the steps in the [installation guide](../../installation.md) to install Kai. It will help you find the latest build and complete the setup.

### Get a Demo App

1. Clone the Cool-store application:

   ```bash
   git clone https://github.com/konveyor-ecosystem/coolstore.git
   ```

   Next, switch to the branch of the Coolstore app that's been partially migrated:

   ```sh
   git checkout partial-migration
   ```

2. Navigate to File > Open in VSCode and locate the folder we just cloned.
   Make sure you have GenAI credentials before you start configuring Kai.

### Configure Konveyor and Start the server

Follow the steps in the [Configuration Guide](../../configuration.md) to set up Kai and start the server. The guide provides in-depth details on customizing the configuration to suit your project’s specific needs.

> [!NOTE]
> If you are following the guided demo for the Coolstore application, ensure you select the following targets during project configuration.

We will analyze the Coolstore application using the following migration targets to identify potential areas for improvement:

- cloud-readiness
- jakarta-ee
- jakarta-ee8
- jakarta-ee9
- quarkus

To verify your target configuration, go to your project directory and open `/.vscode/settings.json`. This serves as a reference for how `settings.json` should look.

```json
{
  "konveyor.analysis.labelSelector": "(konveyor.io/target=cloud-readiness || konveyor.io/target=jakarta-ee || konveyor.io/target=jakarta-ee8 || konveyor.io/target=jakarta-ee9 || konveyor.io/target=quarkus) || (discovery)"
}
```

## Step 2: Run Analysis

Let's perform our initial analysis:

1. Once you have RPC server initialized, navigate to "Konveyor Analysis View" and click `Run Analysis`. Open the command palette by pressing Command + Shift + P to find it.
   ![run_analysis](/docs/scenarios/javaEE_to_quarkus/images/run_analysis.png)

2. The Konveyor Analysis View lists issues, allowing you to filter them by file issues. On the left side, the Konveyor Issue Panel groups files based on similar issues for easier navigation.
   ![konveyor_analysis_view](/docs/scenarios/javaEE_to_quarkus/images/konveyor_analysis_view.png)

If you lose the "Konveyor Analysis View" window, press Command + Shift + P to open the Command Palette, then search for and select the Analysis View window. Alternatively, click the editor icon under the Konveyor Issue panel to reopen it.
![konveyor_analysis_view_1](/docs/scenarios/javaEE_to_quarkus/images/konveyor_analysis_view_1.png)

Once the analysis is complete, you will see many incidents. However, let's focus on fixing only the 6 files necessary to migrate the Coolstore application.

- `src/main/java/com/redhat/coolstore/model/ShoppingCart.java`
- `src/main/java/com/redhat/coolstore/model/InventoryEntity.java`
- `src/main/java/com/redhat/coolstore/service/CatalogService.java`
- `src/main/java/com/redhat/coolstore/service/ShippingService.java`
- `src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java`
- `src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java`

> [!NOTE]
>
> While the file `src/main/java/com/redhat/coolstore/rest/RestApplication.java`
> is flagged, for the purpose of this demo it is okay to skip that file and
> proceed.

The incidents in the above files will provide insights into potential issues or
areas that require attention during the migration process.

> [!NOTE]
>
> Before fixing the issues, keep in mind that results may vary depending on the AI model used. The accuracy and detail of migration suggestions depend on the model’s training data and capabilities. If a different model (e.g., GPT-4, LLaMA-3) is used, the refactoring recommendations may differ.
> In this case, incidents are being fixed using GPT-4o.

### 2.1 Change import namespaces

Open the "Konveyor Analysis View" and search for the `InventoryEntity.java file`. Click on the circled button to resolve all incidents or individual incidents as shown below. In the dropdown menu, different effort levels are available to resolve the incidents, with the default set to 'Low.' As we progress, we will try out different effort levels in the next example.
![request_fix](/docs/scenarios/javaEE_to_quarkus/images/request_fix.png)

The "Resolution Details" window will display the requested fix information as shown below.

![resolution_details](/docs/scenarios/javaEE_to_quarkus/images/resolution_details1.png)

You can view the reasoning behind the suggested changes and additional information provided by Kai.
![resolution_details](/docs/scenarios/javaEE_to_quarkus/images/resolution_details2.png)
Moreover, you can see the additional number of errors that requires your attention and number of modified files.

![resolution_details](/docs/scenarios/javaEE_to_quarkus/images/resolution_details3.png)

Click on the eye symbol to view the differences.
![change_import_namespaces.png](/docs/scenarios/javaEE_to_quarkus/images/change_import_namespaces.png)

Accept the changes by clicking on the symbol shown above on the screenshot. This will trigger analysis and reduce the number of incidents.

The above steps show how Kai simplifies the translation of import namespaces, ensuring seamless automated migration of javax libraries to jakarta persistence
libraries.

Just like we fixed `InventoryEntity.java`, repeat the same steps for `ShoppingCart.java`.

### 2.2 Modify Scope from CDI bean requirements

In this step, we will use Kai to update the scope definitions in `CatalogService.java`, and `ShippingService.java` to align with Quarkus CDI bean requirements. Kai will automate this process, ensuring a smooth migration.

Let's review each file and fix all associated issues one by one. The effort level will remain low. Just like in Step 2.1, we will search for the file and request a resolution.

![cdi_bean_requirement](/docs/scenarios/javaEE_to_quarkus/images/cdi_bean_requirement1.png)

Verify each solution, review the reasoning and additional steps, and ensure the requested changes are applied. In this case, Kai will rerun the analysis and reduce the number of incidents if the changes are compatible.
![cdi_bean_requirement](/docs/scenarios/javaEE_to_quarkus/images/cdi_bean_requirement2.png)

In `CatalogService.java` Stateless EJB is converted to a CDI bean by replacing the @Stateless annotation with a scope @ApplicationScoped.

### 2.3 EJB Remote

Now lets request resolution for the `ShippingService.java` as we did in previous steps. Kai replaced EJBs with REST functionality and updated related imports and annotations.

![shippingService - diff](/docs/scenarios/javaEE_to_quarkus/images/shippingService.png)

Due to the absence of support for Remote EJBs in Quarkus, you will notice that these functionalities are removed and replaced with REST functionality.

### 2.4 JMS to SmallRye

As you can see, there is an option to search for issues where files are grouped by common incidents. Look for "JMS not supported in Quarkus." The files `OrderServiceMDB.java` and `InventoryNotificationMDB.java` are grouped under this issue. However, these files contain additional issues beyond JMS incompatibility.

The incident details indicate that JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/MicroProfile equivalents. Additionally, the project's pom.xml file needs to be updated with the required dependencies. If we introduce a new dependency, it should be properly configured to ensure compatibility with the existing setup.

In such cases, let's leverage Kai's agentic workflow, which helps solve problems in depth. Here, we will request a resolution with medium effort to ensure a more comprehensive fix. Workflow explained [here](#background).

![jsm-to-smallRye](/docs/scenarios/javaEE_to_quarkus/images/jmstosmallrye.png)

This may take longer as Kai is working to resolve a complex problem.

![jsm-to-smallRye](/docs/scenarios/javaEE_to_quarkus/images/jmstosmllrye1.png)

Let's review all the changes one by one.
![jsm-to-smallRye](/docs/scenarios/javaEE_to_quarkus/images/jmstosmallrye2.png)

The migration replaces the JMS-based Message Driven Bean (MDB) with Quarkus SmallRye Reactive Messaging. It removes JMS dependencies, manual connection management, and session handling, replacing them with `@Incoming("orders")` for message processing.

![jsm-to-smallRye](/docs/scenarios/javaEE_to_quarkus/images/jmstosmallrye3.png)

Let's review `pom.xml` file.

> [!NOTE]
> If Kai updates its dependencies and includes SmallRye Reactive Messaging 4.27.0 as an independent dependency, it may not be found in Maven. Since Quarkus already includes SmallRye internally, it is recommended to use `io.quarkus:quarkus-smallrye-reactive-messaging` instead of `io.smallrye.reactive` to ensure compatibility and avoid missing artifacts.
> The required approach may vary based on the LLM model used. Verify and resolve accordingly. The screenshot below shows the expected state.

![jsm-to-smallRye](/docs/scenarios/javaEE_to_quarkus/images/jmstosmallrye4.png)

At the end of this step, the application should be able to compile successfully. Any additional incidents can be ignored. To update dependencies from the repository and compile the project, run the following command

```bash
 mvn clean install -U && mvn compile
```

## Background

### Core Workflow

The Validator serves as the entry point, identifying issues in the repository and re-running the analysis after changes are accepted. It determines task types and generates tasks accordingly.

The TaskManager prioritizes and queues tasks, delegating them to TaskRunners based on their type.

TaskRunners interpret the nature of errors and orchestrate the Agentic Workflow, where multiple specialized agents collaborate to resolve tasks efficiently. Once tasks are executed, the Feedback Loop validates the changes by reanalyzing the codebase, generating new tasks if necessary.

More information available [here](/docs/presentations/2024-11-14-konveyor-community.md).

### Agentic Workflow

The Agentic Workflow enables multiple agents to work together to resolve migration issues. The key agents include:

**AnalyzerAgent**
The initial step in identifying migration issues and generating LLM-based solutions.
Once the LLM response is received, it applies the suggested changes, triggering various symbol resolution tasks.
Upon completion, Validators reanalyze the codebase.

**MavenCompilerAgent**
Handles all non-dependency-related compilation errors.
Example: Resolves SymbolNotFoundError tasks.

**MavenDependencyAgent**
Manages all dependency-related issues detected by both the Analyzer Validator and Compilation Validator.
Example: Resolves PackageDoesNotExistError tasks.

**ReflectionAgent**
Invoked after each task or group of tasks to review and validate the changes (Reflection Iteration 1).
If new tasks arise, such as AnalyzerDependencyRuleViolation, the AnalyzerAgent is called again for further resolution.

### Effort-Based Resolution

The Agentic Workflow operates within a configurable effort level, allowing Kai to adapt its resolution strategy based on user preferences:

- **Low Effort**: Attempts to fix only the detected issues.
- **Medium Effort**: Fixes the detected issues and resolves any new issues caused by the initial fix.
- **High Effort**: Continues resolving issues iteratively until no further problems remain.

Retries occur as part of the implementation process, though they are not currently user-configurable.
![workflow](/docs/scenarios//javaEE_to_quarkus/images/agentic-flow.png)

## Step 3: Deploy app to Kubernetes

Although the app is deployable to any [Kubernetes](https://kubernetes.io/)
distribution. For the sake of simplicity we choose
[minikube](https://minikube.sigs.k8s.io/docs/).

> [!NOTE]
>
> It is assumed that minikube is installed. If not you can follow
> the instructions [here](https://minikube.sigs.k8s.io/docs/start/).

First, start minikube with the docker driver:

```bash
minikube start --driver=docker
```

Next, point your shell to minikube's docker daemon. Kubernetes may not be able
to find the built images if they are not in the same docker daemon as minikube.

```bash
eval $(minikube docker-env)
```

The coolstore requires a PostgreSQL database. To install Postgres into minikube,
we have added deploy scripts. run the scripts in the following order

```bash
kubectl apply -f deploy/kubernetes/persistent-volume.yaml
kubectl apply -f deploy/kubernetes/persistent-volume-claim.yaml
kubectl apply -f deploy/kubernetes/postgresql-deployment.yaml
kubectl apply -f deploy/kubernetes/postgresql-service.yaml

# Wait until the postgres pod is running
watch kubectl get all
```

This should setup the database ready for connections from the coolstore app.

To deploy the app, simply run the following command, it will create a docker
image on the local drive and load the manifests into kubernetes to pull the
image.

```bash
mvn clean compile package -Dquarkus.kubernetes.deploy=true
```

Once deployed, access the app via browser hitting the localhost and port. Note
that it might take a minute when you open the website for the first time. To get
this URL, run the following command:

```bash
minikube service list
```

![deploy app](/docs/scenarios/javaEE_to_quarkus/images/deploy.gif)

## Debug and File Incidents

Please review this [page](/docs/debug.md) for information on Logs, Troubleshooting, and Filing Issues.

## Conclusion

In this demo, we showcased the capability of Kai in facilitating various types
of code migrations within the Coolstore application. By leveraging Kai's
capabilities, organizations can expedite the modernization process. If you are
interested to learn more about our ongoing efforts and future plans, please
reach out to us in the [slack
channel](https://kubernetes.slack.com/archives/CR85S82A2)
