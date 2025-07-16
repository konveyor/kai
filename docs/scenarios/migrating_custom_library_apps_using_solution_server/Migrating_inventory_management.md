# Modernizing Healthcare Applications: Audit Library Migration Using Konveyor AI and Solution Server

## Goal

This scenario demonstrates how **Konveyor AI (Kai)** can assist in modernizing **two healthcare applications** by migrating from an outdated audit logging library (v1) to a modern streaming-based audit library (v2). We will use custom rules with Kai to analyze both applications and generate refactoring recommendations, then leverage the **Solution Server** to demonstrate how migration patterns learned from the first application can be automatically applied to the second application.

## Applications to Modernize

1. **[Medical Device Inventory Management System](https://github.com/savitharaghunathan/inventory_management)** - Manages medical device inventory with comprehensive audit logging. Built with Spring Boot 2 (Java 8) and features REST API endpoints for medical device operations, in-memory storage with sample inventory data, and audit logging using the v1 audit library.

2. **[Electronic Health Record (EHR) System](https://github.com/hhpatel14/ehr_viewer/tree/java8)** - Patient data management system that also uses the same audit logging library for compliance tracking. Built with Spring Boot 2 (Java 8), featuring audit logging for all user actions including login, logout, and patient record access.

This approach showcases the power of Kai's Solution Server in learning from one migration and applying those patterns to similar applications, significantly reducing migration effort and ensuring consistency across healthcare systems. The Solution Server delivers two primary benefits: **Contextual Hints** that surface examples of past migration solutions—including successful user modifications and accepted fixes—enabling Kai to offer actionable hints for difficult or previously unsolved migration problems; and **Migration Success Metrics** that expose detailed success metrics for each migration rule, derived from real-world usage data, enabling IDEs and automation tools to present users with confidence levels for successful migration of given code segments.

## Background

Medical device inventory management systems require robust audit logging for compliance with healthcare regulations (HIPAA, FDA, etc.). The audit trail must capture all device movements, user actions, and patient interactions for regulatory compliance and patient safety.

### The Audit Library Migration Challenge

The current applications use an outdated audit logging library (v1) with the following limitations:

| **v1 (Java 8)**                                 | **v2 (Java 21+)**                |
| ----------------------------------------------- | -------------------------------- |
| Synchronous file-based logging                  | Asynchronous TCP streaming       |
| Builder pattern for `AuditEvent`                | Record-based `AuditEvent`        |
| Convenience methods (`logSuccess`/`logFailure`) | Full `AuditEvent` construction   |
| Local file storage                              | Centralized logging via Logstash |
| Hard-coded configuration                        | Environment-based configuration  |

**Key Migration Drivers:**

- **Performance**: Eliminate blocking audit calls with asynchronous operations
- **Scalability**: Replace file I/O bottlenecks with TCP streaming
- **Compliance**: Enable real-time monitoring for healthcare regulations
- **Security**: Address Java 8 end-of-life concerns
- **Centralization**: Integrate with Logstash for enterprise-wide audit management

### Migration Complexity

The migration from v1 to v2 involves five primary areas of change:

#### Core Migration Areas

1. **Dependency Management**: Upgrade audit library version from 1.0.0 to 2.0.0
2. **Event Creation**: Replace builder pattern with record instantiation
3. **Logger Implementation**: Switch from filesystem to streaming logger
4. **Logging Methods**: Convert synchronous to asynchronous logging
5. **Convenience Methods**: Replace simplified methods with full audit events

#### Impact Assessment

| Migration Area            | Files Affected  | Complexity | Risk Level |
| ------------------------- | --------------- | ---------- | ---------- |
| **Dependencies**          | pom.xml         | Low        | Low        |
| **Event Creation**        | Service classes | Medium     | Medium     |
| **Logger Implementation** | Service classes | High       | High       |
| **Logging Methods**       | Service classes | Medium     | Medium     |
| **Convenience Methods**   | Service classes | High       | Medium     |

## Prerequisites

Ensure you have the following set up:

- [VSCode](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [GenAI credentials](https://github.com/konveyor/kai/blob/main/docs/llm_selection.md#openai-service)
- Java 21 installed
- Maven 3.9+
- [Medical Device Inventory Management System](https://github.com/savitharaghunathan/inventory_management)
- [Kai VSCode IDE extension "0.2.0" or later](https://github.com/konveyor/editor-extensions/releases)
- [Logstash](https://www.elastic.co/downloads/logstash) for audit event processing

## Tutorial Dev Environment

This tutorial was built and tested using the following setup:

- Java Version: OpenJDK 8 & 21
- Maven: 3.9.9
- Spring Boot 2 & 3
- Konveyor AI VSCode Extension Version: 0.2.0
- LLM Model Used: `gpt-o1-mini`

## Step 1: Setup the environment

### 1.1 Clone Inventory Application

```bash
# Clone the Medical Device Inventory Application
git clone https://github.com/savitharaghunathan/inventory_management.git
cd inventory_management

# Switch to the java8 branch
git checkout java8
```

### 1.2 Install and Configure Kai

Follow the [Kai installation guide](https://github.com/konveyor/kai/blob/main/docs/scenarios/demo.md#configure-konveyor) and configure with:

- **Custom Rules**: The audit library migration rules are defined in the `rules/` directory of the inventory application. These rules detect v1 patterns and suggest v2 equivalents. You can select these rules in Kai's configuration
- **Migration Targets**: `openjdk21`

<todo>
### 1.3 enable solution server

## Step 2: Understanding the Custom Rules

### 2.1 Audit Library Migration Rules

The custom rules detect v1 audit library patterns and suggest v2 equivalents:

#### Rule 1: Dependency Version Upgrade

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
labels:
  - konveyor.io/source=openjdk8
  - konveyor.io/target=openjdk21
```

**Migration Point:**

- **File**: `pom.xml`
- **Change**: Update dependency version from 1.0.0 to 2.0.0
- **Impact**: Enables Java 21 features and new API capabilities

#### Rule 2: Audit Event Builder Pattern

```yaml
ruleID: audit-logging-0002
description: Replace deprecated `AuditEvent.builder()` with direct Java 21 record instantiation
category: mandatory
effort: 3
when:
  java.referenced:
    pattern: com.enterprise.audit.logging.model.AuditEvent.builder
    location: IMPORT
message: The `AuditEvent.builder()` pattern is deprecated. Instantiate the `AuditEvent` record directly (e.g. `new AuditEvent(...)`).
labels:
  - konveyor.io/source=openjdk8
  - konveyor.io/target=openjdk21
```

**Migration Point:**

- **Pattern**: Replace builder pattern with direct record instantiation
- **Before**: `AuditEvent.builder().eventType("TYPE").build()`
- **After**: `new AuditEvent(timestamp, "TYPE", userId, ...)`
- **Impact**: Leverages Java 21 records for type safety and performance

#### Rule 3: Logger Implementation

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
labels:
  - konveyor.io/source=openjdk8
  - konveyor.io/target=openjdk21
```

**Migration Point:**

- **Pattern**: Replace FileSystemAuditLogger with StreamableAuditLogger
- **Before**: `new FileSystemAuditLogger(config)`
- **After**: `new StreamableAuditLogger(config)`
- **Impact**: Enables TCP streaming to centralized logging infrastructure

#### Rule 4: Synchronous to Asynchronous Logging

```yaml
ruleID: audit-logging-0004
description: Use non-blocking `logEventAsync(event)` instead of synchronous `logEvent(event)`
category: mandatory
effort: 3
when:
  java.referenced:
    pattern: com.enterprise.audit.logging.service.FileSystemAuditLogger.logEvent
    location: METHOD_CALL
message: The synchronous `logEvent(event)` method should be replaced. Use the non-blocking `logEventAsync(event)` for better performance.
labels:
  - konveyor.io/source=openjdk8
  - konveyor.io/target=openjdk21
```

**Migration Point:**

- **Pattern**: Replace synchronous logging with asynchronous
- **Before**: `auditLogger.logEvent(auditEvent)`
- **After**: `auditLogger.logEventAsync(auditEvent)`
- **Impact**: Improves application performance by eliminating blocking operations

#### Rule 5: Convenience Methods

```yaml
ruleID: audit-logging-0005
description: Replace legacy `logSuccess` or `logFailure` methods with a full `AuditEvent` record
category: mandatory
effort: 3
when:
  or:
    - java.referenced:
        pattern: com.enterprise.audit.logging.service.FileSystemAuditLogger.logSuccess
        location: METHOD_CALL
    - java.referenced:
        pattern: com.enterprise.audit.logging.service.FileSystemAuditLogger.logFailure
        location: METHOD_CALL
message: Legacy convenience methods (logSuccess, logFailure) are removed. Construct a full `AuditEvent` record and use logEventAsync instead.
labels:
  - konveyor.io/source=openjdk8
  - konveyor.io/target=openjdk21
```

**Migration Point:**

- **Pattern**: Replace convenience methods with full audit event construction
- **Before**: `auditLogger.logSuccess("TYPE", "ACTION", "RESOURCE", "MESSAGE")`
- **After**: Full `AuditEvent` construction with all required fields

## Step 3: Run Analysis

### 3.1 Initial Analysis Results

<todo>

### 3.2 Applying Migration Fixes

<todo>
