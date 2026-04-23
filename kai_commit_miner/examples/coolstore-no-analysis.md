# KAI Commit Miner Report

**Migration** (Inferred from manifest diffs): Migration from Java EE 7 monolithic application to Quarkus 3.12.3 microservices framework. The project changes from WAR packaging to JAR, replaces Java EE APIs with Quarkus extensions (quarkus-arc for CDI, quarkus-resteasy for REST, quarkus-hibernate-orm for JPA), updates Java version from 1.8 to 21, and relocates web resources from webapp to META-INF/resources for Quarkus static resource serving.

**Source labels:** javaee, eap6, eap7
**Target labels:** quarkus, quarkus3, jakarta-ee, cloud-readiness, eap8

**Label selector:** `konveyor.io/target=quarkus || konveyor.io/target=quarkus3 || konveyor.io/target=jakarta-ee || konveyor.io/target=cloud-readiness || konveyor.io/target=eap8`

## Summary

| Metric               | Count |
| -------------------- | ----- |
| Violations resolved  | 0     |
| Files changed        | 2558  |
| Violation types      | 0     |
| Hints generated      | 0     |
| Hints skipped        | 0     |
| New rules discovered | 25    |

## New Rule Candidates (25)

Proposed analyzer-lsp rules detecting pre-migration patterns. 24 high-relevance, 1 lower.

### `mined-javax-jms-messagelistener` — high

**MessageListener interface implementation for JMS message handling**

> MessageListener is the traditional Java EE way of handling JMS messages, needs to be replaced with MicroProfile Reactive Messaging in Quarkus

```yaml
- ruleID: mined-javax-jms-messagelistener
  description: MessageListener interface implementation for JMS message handling
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: IMPLEMENTS
      pattern: javax.jms.MessageListener
  message: |
    Replace MessageListener with MicroProfile Reactive Messaging @Incoming annotation for message handling in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-jms-message-parameter` — high

**JMS Message parameter in onMessage method**

> Traditional JMS Message handling pattern needs to be converted to direct message payload handling in Quarkus reactive messaging

```yaml
- ruleID: mined-javax-jms-message-parameter
  description: JMS Message parameter in onMessage method
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: PARAMETER
      pattern: javax.jms.Message
  message: |
    Replace javax.jms.Message parameter with direct message payload type and use @Incoming annotation from MicroProfile Reactive Messaging

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-messagedriven-annotation` — high

**MessageDriven EJB annotation usage**

> MessageDriven EJBs are Java EE specific and need to be replaced with MicroProfile Reactive Messaging in Quarkus

```yaml
- ruleID: mined-messagedriven-annotation
  description: MessageDriven EJB annotation usage
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.MessageDriven
  message: |
    Replace @MessageDriven EJB with @ApplicationScoped component and @Incoming annotation from MicroProfile Reactive Messaging

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-activationconfigproperty-annotation` — high

**ActivationConfigProperty annotation for message driven beans**

> ActivationConfigProperty is specific to Java EE MessageDriven beans and needs to be replaced with Quarkus reactive messaging configuration

```yaml
- ruleID: mined-activationconfigproperty-annotation
  description: ActivationConfigProperty annotation for message driven beans
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.ActivationConfigProperty
  message: |
    Replace @ActivationConfigProperty with MicroProfile Reactive Messaging configuration properties

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-stateful-annotation` — high

**Stateful EJB annotation usage**

> Stateful EJBs are Java EE specific and need to be replaced with appropriate CDI scopes in Quarkus

```yaml
- ruleID: mined-ejb-stateful-annotation
  description: Stateful EJB annotation usage
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Stateful
  message: |
    Replace @Stateful EJB with @SessionScoped CDI bean for session-scoped state management

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-stateless-annotation` — high

**Stateless EJB annotation usage**

> Stateless EJBs are Java EE specific and need to be replaced with appropriate CDI scopes in Quarkus

```yaml
- ruleID: mined-ejb-stateless-annotation
  description: Stateless EJB annotation usage
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Stateless
  message: |
    Replace @Stateless EJB with @ApplicationScoped or @RequestScoped CDI bean depending on usage pattern

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-singleton-annotation` — high

**Singleton EJB annotation usage**

> EJB Singleton needs to be replaced with CDI Singleton in Quarkus

```yaml
- ruleID: mined-ejb-singleton-annotation
  description: Singleton EJB annotation usage
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Singleton
  message: |
    Replace @javax.ejb.Singleton with @jakarta.inject.Singleton for CDI-based singleton pattern

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-startup-annotation` — high

**EJB Startup annotation usage**

> EJB Startup annotation needs to be replaced with Quarkus startup annotation

```yaml
- ruleID: mined-ejb-startup-annotation
  description: EJB Startup annotation usage
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Startup
  message: |
    Replace @javax.ejb.Startup with @io.quarkus.runtime.Startup for application startup initialization

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-transactionmanagement-annotation` — medium

**TransactionManagement annotation usage**

> TransactionManagement is often not needed in Quarkus CDI beans as transaction management is simplified

```yaml
- ruleID: mined-ejb-transactionmanagement-annotation
  description: TransactionManagement annotation usage
  category: optional
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.TransactionManagement
  message: |
    Remove @TransactionManagement annotation as Quarkus CDI beans use simplified transaction management with @Transactional

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-resource-annotation-datasource` — high

**Resource annotation for DataSource injection**

> Resource annotation with mappedName is Java EE specific and needs to be replaced with CDI injection in Quarkus

```yaml
- ruleID: mined-resource-annotation-datasource
  description: Resource annotation for DataSource injection
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.annotation.Resource
  message: |
    Replace @Resource annotation with @Inject for CDI-based dependency injection in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jms-jmscontext-injection` — high

**JMSContext injection for message sending**

> JMSContext is traditional Java EE JMS API that needs to be replaced with MicroProfile Reactive Messaging in Quarkus

```yaml
- ruleID: mined-jms-jmscontext-injection
  description: JMSContext injection for message sending
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: FIELD
      pattern: javax.jms.JMSContext
  message: |
    Replace JMSContext with MicroProfile Reactive Messaging Emitter for sending messages

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jms-topic-resource` — high

**JMS Topic resource lookup**

> JMS Topic resource lookup is Java EE specific and needs to be replaced with reactive messaging channels

```yaml
- ruleID: mined-jms-topic-resource
  description: JMS Topic resource lookup
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: FIELD
      pattern: javax.jms.Topic
  message: |
    Replace JMS Topic with MicroProfile Reactive Messaging @Channel and Emitter for message publishing

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-remote-annotation` — high

**Remote EJB interface annotation**

> Remote EJB interfaces need to be replaced with REST services in microservices architecture

```yaml
- ruleID: mined-ejb-remote-annotation
  description: Remote EJB interface annotation
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Remote
  message: |
    Replace @Remote EJB interface with REST endpoints using JAX-RS annotations (@Path, @POST, etc.)

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-weblogic-applicationlifecyclelistener` — high

**WebLogic ApplicationLifecycleListener usage**

> WebLogic-specific lifecycle listener needs to be replaced with Quarkus lifecycle events

```yaml
- ruleID: mined-weblogic-applicationlifecyclelistener
  description: WebLogic ApplicationLifecycleListener usage
  category: mandatory
  effort: 6
  when:
    java.referenced:
      location: EXTENDS
      pattern: weblogic.application.ApplicationLifecycleListener
  message: |
    Replace WebLogic ApplicationLifecycleListener with Quarkus lifecycle events (@Observes StartupEvent, @Observes ShutdownEvent)

  labels:
    - konveyor.io/source=weblogic
    - konveyor.io/target=quarkus
```

### `mined-weblogic-applicationlifecycleevent` — high

**WebLogic ApplicationLifecycleEvent usage**

> WebLogic-specific lifecycle event needs to be replaced with Quarkus lifecycle events

```yaml
- ruleID: mined-weblogic-applicationlifecycleevent
  description: WebLogic ApplicationLifecycleEvent usage
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: PARAMETER
      pattern: weblogic.application.ApplicationLifecycleEvent
  message: |
    Replace WebLogic ApplicationLifecycleEvent with Quarkus StartupEvent or ShutdownEvent

  labels:
    - konveyor.io/source=weblogic
    - konveyor.io/target=quarkus
```

### `mined-persistencecontext-annotation` — high

**PersistenceContext annotation for EntityManager injection**

> PersistenceContext is Java EE specific and needs to be replaced with CDI injection in Quarkus

```yaml
- ruleID: mined-persistencecontext-annotation
  description: PersistenceContext annotation for EntityManager injection
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.persistence.PersistenceContext
  message: |
    Replace @PersistenceContext with @Inject for EntityManager injection in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-weblogic-noncataloglogger` — high

**WebLogic NonCatalogLogger usage**

> WebLogic-specific logging needs to be replaced with standard Java logging or Quarkus logging

```yaml
- ruleID: mined-weblogic-noncataloglogger
  description: WebLogic NonCatalogLogger usage
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: TYPE
      pattern: weblogic.i18n.logging.NonCatalogLogger
  message: |
    Replace WebLogic NonCatalogLogger with standard java.util.logging.Logger or Quarkus logging

  labels:
    - konveyor.io/source=weblogic
    - konveyor.io/target=quarkus
```

### `mined-javaee-beans-xml-webapp` — high

**Detects Java EE beans.xml file in webapp/WEB-INF directory**

> The beans.xml file in webapp/WEB-INF is Java EE specific and needs to be relocated or removed in Quarkus migration

```yaml
- ruleID: mined-javaee-beans-xml-webapp
  description: Detects Java EE beans.xml file in webapp/WEB-INF directory
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: "*/webapp/WEB-INF/beans.xml"
      pattern: .*xmlns="http://xmlns\.jcp\.org/xml/ns/javaee".*
  message: |
    Java EE beans.xml configuration detected in webapp/WEB-INF directory. In Quarkus, CDI is enabled by default and beans.xml should be moved to src/main/resources/META-INF/beans.xml if still needed, or removed entirely as Quarkus enables CDI automatically.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javaee-persistence-xml-jta-datasource` — high

**Detects Java EE persistence.xml with JTA datasource configuration**

> Java EE persistence.xml with JTA datasource references needs to be replaced with Quarkus datasource configuration in application.properties

```yaml
- ruleID: mined-javaee-persistence-xml-jta-datasource
  description: Detects Java EE persistence.xml with JTA datasource configuration
  category: mandatory
  effort: 5
  when:
    builtin.filecontent:
      filePattern: "*/persistence.xml"
      pattern: .*<jta-data-source>java:jboss/.*
  message: |
    Java EE JTA datasource configuration detected in persistence.xml. In Quarkus, datasource configuration should be moved to application.properties using quarkus.datasource.* properties instead of JNDI references like java:jboss/datasources/*.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javaee-persistence-xml-javax-properties` — high

**Detects javax.persistence properties in persistence.xml**

> javax.persistence properties in persistence.xml need to be migrated to Quarkus hibernate-orm configuration properties

```yaml
- ruleID: mined-javaee-persistence-xml-javax-properties
  description: Detects javax.persistence properties in persistence.xml
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: "*/persistence.xml"
      pattern: .*javax\.persistence\.schema-generation\..*
  message: |
    javax.persistence properties detected in persistence.xml. In Quarkus, these should be replaced with quarkus.hibernate-orm.* properties in application.properties (e.g., javax.persistence.schema-generation.database.action becomes quarkus.hibernate-orm.database.generation).

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javaee-web-xml-webapp` — high

**Detects Java EE web.xml configuration file**

> web.xml is Java EE specific configuration that is typically not needed in Quarkus applications

```yaml
- ruleID: mined-javaee-web-xml-webapp
  description: Detects Java EE web.xml configuration file
  category: mandatory
  effort: 4
  when:
    builtin.filecontent:
      filePattern: "*/webapp/WEB-INF/web.xml"
      pattern: .*xmlns="http://java\.sun\.com/xml/ns/javaee".*
  message: |
    Java EE web.xml configuration detected. In Quarkus, most web.xml configurations are not needed as Quarkus uses different mechanisms for web application configuration. Static resources should be moved to src/main/resources/META-INF/resources and servlet configurations should be replaced with Quarkus-specific annotations or properties.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javaee-persistence-xml-version-21` — high

**Detects Java EE persistence.xml version 2.1**

> Java EE persistence.xml version 2.1 is specific to Java EE and needs migration to Quarkus configuration approach

```yaml
- ruleID: mined-javaee-persistence-xml-version-21
  description: Detects Java EE persistence.xml version 2.1
  category: mandatory
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "*/persistence.xml"
      pattern: .*xmlns="http://xmlns\.jcp\.org/xml/ns/persistence".*version="2\.1".*
  message: |
    Java EE persistence.xml version 2.1 detected. In Quarkus, persistence configuration should be moved from persistence.xml to application.properties using quarkus.hibernate-orm.* and quarkus.datasource.* properties.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-webapp-static-resources-location` — high

**Detects static web resources in src/main/webapp directory that need relocation for Quarkus**

> This is a fundamental structural change required when migrating from Java EE WAR packaging to Quarkus JAR packaging. Quarkus serves static resources from META-INF/resources instead of webapp directory.

```yaml
- ruleID: mined-webapp-static-resources-location
  description: Detects static web resources in src/main/webapp directory that need relocation for Quarkus
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: src/main/webapp/**/*
  message: |
    Static web resources in src/main/webapp/ directory must be relocated to src/main/resources/META-INF/resources/ for Quarkus microservices framework. Quarkus uses JAR packaging and serves static content from the META-INF/resources directory within the JAR, unlike traditional Java EE applications that use WAR packaging with webapp directory.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jsp-scriptlet-in-html` — high

**JSP scriptlet code embedded in HTML files**

> JSP scriptlets are Java EE web technology that needs to be replaced with modern templating or REST endpoints in Quarkus microservices

```yaml
- ruleID: mined-jsp-scriptlet-in-html
  description: JSP scriptlet code embedded in HTML files
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: .*\.(html|htm)$
      pattern: <%.*%>
  message: |
    JSP scriptlets in HTML files are not supported in Quarkus. Replace with:
    - Qute templating engine for server-side rendering
    - REST endpoints with JSON responses for AJAX calls
    - Static HTML with JavaScript for client-side functionality

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jsp-files` — high

**JavaServer Pages (JSP) files**

> JSP files are Java EE web view technology that is not supported in Quarkus and must be replaced with modern alternatives

```yaml
- ruleID: mined-jsp-files
  description: JavaServer Pages (JSP) files
  category: mandatory
  effort: 5
  when:
    builtin.filecontent:
      filePattern: .*\.jsp$
      pattern: .*
  message: |
    JSP files are not supported in Quarkus. Replace with:
    - Qute templating engine for server-side HTML generation
    - Static HTML files served from META-INF/resources
    - REST endpoints returning JSON data for frontend consumption
    - Modern frontend frameworks (React, Vue, Angular) for dynamic UIs

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

## Hints (0 generated, 0 skipped)
