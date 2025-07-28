# Migrating healthcare apps using Kai solution server

Konveyor AI (kai) is Konveyor's approach to easing modernization of application source code to a new target by leveraging LLMs with guidance from static code analysis augmented with data in Konveyor that helps to learn how an Organization solved a similar problem in the past.

- [Migrating healthcare apps using Kai solution server](#migrating-healthcare-apps-using-kai-solution-server)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Step 1: Setup](#step-1-setup)
    - [Clone the Inventory Management System](#clone-the-inventory-management-system)
    - [Clone the EHR Viewer Application](#clone-the-ehr-viewer-application)
  - [Step 2: Migration using solution server](#step-2-migration-using-solution-server)
    - [2.1 Migrate Inventory Management](#21-migrate-inventory-management)
    - [2.2 Migrate EHR Viewer](#22-migrate-ehr-viewer)
  - [Step 3: Verify Solution Server Benefits](#step-3-verify-solution-server-benefits)
  - [Step 4: Deploy and Run the Applications](#step-4-deploy-and-run-the-applications)
  - [Conclusion](#conclusion)

## Overview

In this scenario, we will showcase the capabilities of Kai's **Solution Server** in learning from one migration and applying those patterns to accelerate similar migrations. We will demonstrate how the Solution Server captures successful migration patterns and provides contextual hints and success metrics for future migrations.

We will focus on migrating two healthcare applications that use a custom audit logging library, showing how the Solution Server learns from the first migration and significantly accelerates the second one.

### Solution Server Capabilities

The Solution Server delivers two primary benefits to users of Kai:

- **Contextual Hints**: It surfaces examples of past migration solutions—including successful user modifications and accepted fixes—enabling Kai to offer actionable hints for difficult or previously unsolved migration problems.

- **Migration Success Metrics**: It exposes detailed success metrics for each migration rule, derived from past migrations. These metrics present users with a "confidence level" or likelihood of Kai successfully migrating a given code segment.

### Custom Rules for Audit Library Migration

This scenario uses custom migration rules specifically designed for the audit logging library migration:

#### Rule 1: Dependency Version Upgrade (`audit-logging-0001`)

```yaml
ruleID: audit-logging-0001
description: Detects Maven dependency on v1.x of audit-logging-library and suggests upgrading to 2.x.x (Java 21+)
category: mandatory
effort: 1
when:
  java.dependency:
    name: com.enterprise.audit-logging-library
    lowerbound: "1.0.0"
    upperbound: "1.9.0"
message: The `audit-logging-library` version {{dependency.version}} is outdated. Please upgrade to 2.0.0.
```

**What it detects**: Maven dependencies using audit library v1.x
**Solution Server learning**: Captures successful dependency upgrade patterns and version compatibility configurations

#### Rule 2: Logger Implementation (`audit-logging-0003`)

```yaml
ruleID: audit-logging-0003
description: Replace `FileSystemAuditLogger` instantiation with `StreamableAuditLogger` over TCP
category: mandatory
effort: 3
when:
  java.referenced:
    pattern: com.enterprise.audit.logging.service.FileSystemAuditLogger
    location: IMPORT
message: Direct instantiation of `FileSystemAuditLogger` is deprecated. Use `StreamableAuditLogger` configured for TCP streaming.
```

**What it detects**: Usage of deprecated `FileSystemAuditLogger`
**Solution Server learning**: Captures configuration patterns for `StreamableAuditLogger` including host, port, and protocol settings

## Prerequisites

- [VSCode](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- AI credentials
- [Maven](https://maven.apache.org/install.html)
- Kai with Solution Server enabled
- Java 21
- Maven 3.6+
- Logstash running on port 5000 (for audit streaming)

Additionally, you will need to have the Kai IDE plugin installed in VSCode with Solution Server enabled.
Download the latest from [here](https://github.com/konveyor/editor-extensions/releases).

## Step 1: Setup

TODO: setup Kai

### Clone the Inventory Management System

1. Clone the Medical Device Inventory Management application:

   ```bash
   git clone https://github.com/savitharaghunathan/inventory_management.git
   cd inventory_management
   git checkout partial
   ```

2. Navigate to File > Open in VSCode and locate the folder we just cloned.

### Clone the EHR Viewer Application

1. Clone the EHR Viewer application:

   ```bash
   git clone https://github.com/hhpatel14/ehr_viewer.git
   cd ehr_viewer
   git checkout partial
   ```

2. Open this folder in a separate VSCode window.

## Step 2: Migration using solution server

### 2.1 Migrate Inventory Management

1. **Run Analysis**: Start Kai analysis on the inventory management project
   - Select migration targets: `openjdk21`
   - Custom rules: Select `rules` folder for the cutom rules

Start the analyzer and Run analysis. the vilation will include `audit-logging-0001` and `audit-logging-0003`

#### The Analysis Results

Kai quickly identifies several migration issues in the codebase. The analysis shows violations related to the outdated audit library dependency and deprecated logger implementation patterns.

#### Fix 1: Dependency Upgrade Challenge

The first violation appears straightforward - the `pom.xml` file contains audit library v1.0.0 which needs upgrading to v2.0.0. When you click the tool icon to request a fix, Kai's LLM handles this well since Maven dependency patterns are common in its training data. The fix is applied successfully, updating both the library version and Java compiler settings to version 21.

Behind the scenes, the Solution Server captures this successful upgrade pattern, noting the specific version combination and compatibility requirements.

#### Fix 2: The Logger Implementation Dilemma

The second violation proves more challenging. Kai detects the deprecated `FileSystemAuditLogger` and suggests replacing it with `StreamableAuditLogger`. However, when you request a fix, the LLM's suggestion is incomplete:

```java
// LLM's generic suggestion - incomplete
auditLogger = new StreamableAuditLogger(config);
```

The problem becomes clear: the LLM doesn't know how to properly configure the custom `AuditConfiguration` class. This enterprise-specific library isn't part of the LLM's public training data.

Update the migration susstestion witj the following configuration:

```java
// Manual intervention required
AuditConfiguration config = new AuditConfiguration();
config.setStreamHost(System.getenv().getOrDefault("AUDIT_STREAM_HOST", "localhost"));
config.setStreamPort(Integer.parseInt(System.getenv().getOrDefault("AUDIT_STREAM_PORT", "5000")));
config.setStreamProtocol(System.getenv().getOrDefault("AUDIT_STREAM_PROTOCOL", "tcp"));
auditLogger = new StreamableAuditLogger(config);
```

#### Solution Server Learning

As you accept each fix from Kai, either as-is or modiefied, the Solution Server captures every pattern. This learning process transforms your manual work into reusable knowledge for future migrations.

### 2.2 Migrate EHR Viewer

Open the EHR viewer project in a separate VSCode window and run the same Kai analysis with identical migration targets and custom rules.

#### Fix 1: Dependency Upgrade

The dependency upgrade violation appears again, but this time Kai displays a confidence level next to the suggested fix. The LLM still handles this well, but now you have validation that this specific version combination has been proven to work in a similar healthcare application.

#### Fix 2: Logger Implementation

Here's where the Solution Server truly shines. The same `FileSystemAuditLogger` violation appears, but instead of the incomplete suggestion you saw before, Kai now provides the complete, working configuration:

```java
// Previously required manual work, now auto-generated
AuditConfiguration config = new AuditConfiguration();
config.setStreamHost(System.getenv().getOrDefault("AUDIT_STREAM_HOST", "localhost"));
config.setStreamPort(Integer.parseInt(System.getenv().getOrDefault("AUDIT_STREAM_PORT", "5000")));
config.setStreamProtocol(System.getenv().getOrDefault("AUDIT_STREAM_PROTOCOL", "tcp"));
auditLogger = new StreamableAuditLogger(config);
```

What previously required manual research and implementation is now automatically suggested.

#### Additional Accelerated Fixes

As you continue through the EHR migration, the acceleration becomes even more apparent:

#### The Power of Cross-Application Learning

What makes this remarkable is that the Solution Server doesn't just copy patterns - it adapts them. The learned configuration patterns are applied to the EHR context while maintaining the technical correctness that was manually validated in the inventory management migration.

The migration that previously would have required the same manual research and domain expertise now flows smoothly, with high-confidence suggestions based on proven patterns.

## Step 3: Verify Solution Server Benefits

### Compare Migration Experiences

| First Migration (Inventory Management) | Second Migration (EHR Viewer)             |
| -------------------------------------- | ----------------------------------------- |
| Manual pattern discovery               | Contextual hints from Solution Server     |
| Trial and error with configurations    | Pre-validated patterns and configurations |
| Time-intensive troubleshooting         | Significantly faster resolution           |

### Measure the Acceleration

Track the differences:

- **Time to completion**: EHR migration is comparitvely faster
- **Error rate**: Reduced failed attempts on similar violations
- **Consistency**: Both applications use identical audit patterns

### Solution Server Knowledge Base

After both migrations, the Solution Server contains:

- **Audit library migration patterns** for healthcare applications
- **Success metrics** showing high confidence for similar future migrations

## Step 4: Deploy and Run the Applications

### 4.1 Configure Logstash for Audit Streaming

Both applications now use the v2 audit library with TCP streaming capabilities. Set up Logstash to receive and process audit events.

#### Start Logstash Container

```bash
podman run -d --name logstash -p 5000:5000 \
  -v $(pwd)/logstash.conf:/usr/share/logstash/pipeline/logstash.conf \
  -v $(pwd)/logstash.yml:/usr/share/logstash/config/logstash.yml \
  docker.elastic.co/logstash/logstash:8.11.0
```

### 4.2 Build and Run Inventory Management

1. **Build the Application**

   ```bash
   cd inventory_management
   mvn clean compile
   ```

2. **Start the Application**

   ```bash
   mvn spring-boot:run
   ```

3. **Test the API**
   ```bash
   curl -X GET "http://localhost:8080/api/medical-devices?userId=user123"
   ```

### 4.3 Build and Run EHR Viewer

1. **Build the Application**

   ```bash
   cd ehr_viewer
   mvn clean compile
   ```

2. **Start the Application**

   ```bash
   mvn spring-boot:run
   ```

3. **Test the Web UI**
   - Navigate to: `http://localhost:8081/ui/login`
   - Use sample credentials: `johndoe` / `password1`
   - Follow the steps from the [EHR README](https://github.com/hhpatel14/ehr_viewer/tree/java21?tab=readme-ov-file#1-login)

### 4.4 Verify Audit Streaming

Check that both applications are sending audit events to Logstash:

```bash
# Check inventory management audit events
podman logs logstash | grep "InventoryService"

# Check EHR viewer audit events
podman logs logstash | grep "UserService"
```

Expected output shows structured JSON audit events with consistent patterns learned by the Solution Server:

```json
{"timestamp":"2024-01-15T10:30:45.123Z","event_type":"MEDICAL_DEVICE_VIEW","application":"MedicalDeviceInventory"...}
{"timestamp":"2024-01-15T10:31:12.456Z","event_type":"PATIENT_RECORD_VIEW","application":"EHRViewer"...}
```

## Conclusion

In this scenario, we showcased the power of Kai's **Solution Server** in learning from one migration and accelerating similar ones. The Solution Server captured successful patterns from the inventory management migration and applied them to dramatically speed up the EHR viewer migration.

Key benefits demonstrated:

- **Cross-application learning**: Patterns learned from one app accelerate others
- **Contextual hints**: Domain-specific guidance based on past successes
- **Success metrics**: Confidence levels help prioritize migration efforts
- **Consistency**: Ensures uniform patterns across related applications

By the end of this scenario, you will understand how Kai's Solution Server transforms migration from a repetitive manual process into an accelerating, learning-based workflow that gets smarter with each project.
