# KAI Commit Miner Report

**Migration** (Inferred from manifest diffs): Migration from a traditional Java EE 7 monolithic web application to Quarkus 3.12.3. The project structure changes from a WAR-packaged application using Java EE APIs to a Quarkus-based application with modern Jakarta EE standards. Key changes include replacing Java EE dependencies with Quarkus extensions (quarkus-arc, quarkus-resteasy, quarkus-hibernate-orm), updating Java version from 1.8 to 21, moving static web resources from src/main/webapp to src/main/resources/META-INF/resources, and adding Quarkus-specific build plugins and native compilation support.

**Source labels:** javaee, javaee7
**Target labels:** quarkus, quarkus3, jakarta-ee, cloud-readiness

**Label selector:** `konveyor.io/target=quarkus || konveyor.io/target=quarkus3 || konveyor.io/target=jakarta-ee || konveyor.io/target=cloud-readiness`

## Summary

| Metric               | Count |
| -------------------- | ----- |
| Violations resolved  | 0     |
| Files changed        | 2558  |
| Violation types      | 0     |
| Hints generated      | 0     |
| Hints skipped        | 0     |
| New rules discovered | 27    |

## New Rule Candidates (27)

Proposed analyzer-lsp rules detecting pre-migration patterns. 25 high-relevance, 2 lower.

### `mined-javax-ejb-stateless-to-applicationscoped` — high

**Detects @Stateless EJB annotation usage**

> Direct Java EE to Jakarta EE migration pattern - @Stateless EJB needs to be replaced with CDI @ApplicationScoped in Quarkus

```yaml
- ruleID: mined-javax-ejb-stateless-to-applicationscoped
  description: Detects @Stateless EJB annotation usage
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ejb.Stateless
  message: |
    Replace @Stateless EJB annotation with @ApplicationScoped from jakarta.enterprise.context.ApplicationScoped for CDI-based services in Quarkus

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-ejb-stateful-to-sessionscoped` — high

**Detects @Stateful EJB annotation usage**

> Direct Java EE to Jakarta EE migration pattern - @Stateful EJB needs to be replaced with CDI @SessionScoped in Quarkus

```yaml
- ruleID: mined-javax-ejb-stateful-to-sessionscoped
  description: Detects @Stateful EJB annotation usage
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ejb.Stateful
  message: |
    Replace @Stateful EJB annotation with @SessionScoped from jakarta.enterprise.context.SessionScoped for stateful services in Quarkus

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-ejb-messagedriven-to-reactive-messaging` — high

**Detects @MessageDriven EJB annotation usage**

> Core messaging pattern migration - @MessageDriven EJBs need to be replaced with MicroProfile Reactive Messaging in Quarkus

```yaml
- ruleID: mined-javax-ejb-messagedriven-to-reactive-messaging
  description: Detects @MessageDriven EJB annotation usage
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ejb.MessageDriven
  message: |
    Replace @MessageDriven EJB with MicroProfile Reactive Messaging using @Incoming annotation and remove MessageListener interface

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-ejb-startup-to-quarkus-startup` — high

**Detects @Startup EJB annotation usage**

> Direct migration pattern - javax.ejb.Startup needs to be replaced with io.quarkus.runtime.Startup

```yaml
- ruleID: mined-javax-ejb-startup-to-quarkus-startup
  description: Detects @Startup EJB annotation usage
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ejb.Startup
  message: |
    Replace @Startup from javax.ejb with @Startup from io.quarkus.runtime.Startup for application startup beans

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-jms-messagelistener-interface` — high

**Detects MessageListener interface usage**

> Core messaging migration - MessageListener interface is part of the JMS API that needs to be replaced with Reactive Messaging

```yaml
- ruleID: mined-javax-jms-messagelistener-interface
  description: Detects MessageListener interface usage
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.jms.MessageListener
  message: |
    Remove MessageListener interface and replace onMessage(Message) method with @Incoming reactive messaging method

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-resource-annotation` — high

**Detects @Resource annotation usage for resource injection**

> Resource injection pattern change - @Resource needs to be replaced with @Inject in Quarkus CDI

```yaml
- ruleID: mined-javax-resource-annotation
  description: Detects @Resource annotation usage for resource injection
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.annotation.Resource
  message: |
    Replace @Resource annotation with @Inject for dependency injection in Quarkus

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-jms-context-usage` — high

**Detects JMSContext usage for messaging**

> Messaging migration - JMSContext needs to be replaced with MicroProfile Reactive Messaging Emitter

```yaml
- ruleID: mined-javax-jms-context-usage
  description: Detects JMSContext usage for messaging
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.jms.JMSContext
  message: |
    Replace JMSContext with MicroProfile Reactive Messaging Emitter for sending messages

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-ejb-remote-interface` — high

**Detects @Remote EJB annotation usage**

> EJB remote interface migration - @Remote EJBs need to be converted to REST services in Quarkus

```yaml
- ruleID: mined-javax-ejb-remote-interface
  description: Detects @Remote EJB annotation usage
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ejb.Remote
  message: |
    Replace @Remote EJB with REST endpoint using JAX-RS @Path and @POST/@GET annotations for remote service access

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-persistence-to-jakarta-persistence` — high

**Detects javax.persistence package usage**

> Direct package migration - javax.persistence needs to be replaced with jakarta.persistence in Jakarta EE

```yaml
- ruleID: mined-javax-persistence-to-jakarta-persistence
  description: Detects javax.persistence package usage
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.persistence.EntityManager
  message: |
    Replace javax.persistence imports with jakarta.persistence for Jakarta EE compatibility

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-enterprise-to-jakarta-enterprise` — high

**Detects javax.enterprise package usage**

> Direct package migration - javax.enterprise needs to be replaced with jakarta.enterprise in Jakarta EE

```yaml
- ruleID: mined-javax-enterprise-to-jakarta-enterprise
  description: Detects javax.enterprise package usage
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.enterprise.context.ApplicationScoped
  message: |
    Replace javax.enterprise imports with jakarta.enterprise for Jakarta EE compatibility

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-inject-to-jakarta-inject` — high

**Detects javax.inject package usage**

> Direct package migration - javax.inject needs to be replaced with jakarta.inject in Jakarta EE

```yaml
- ruleID: mined-javax-inject-to-jakarta-inject
  description: Detects javax.inject package usage
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.inject.Inject
  message: |
    Replace javax.inject imports with jakarta.inject for Jakarta EE compatibility

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-weblogic-lifecycle-listener` — high

**Detects WebLogic ApplicationLifecycleListener usage**

> Application server specific code - WebLogic lifecycle listeners need to be replaced with Quarkus startup events

```yaml
- ruleID: mined-weblogic-lifecycle-listener
  description: Detects WebLogic ApplicationLifecycleListener usage
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: IMPORT
      pattern: weblogic.application.ApplicationLifecycleListener
  message: |
    Replace WebLogic ApplicationLifecycleListener with Quarkus startup/shutdown events or @PostConstruct/@PreDestroy methods

  labels:
    - konveyor.io/source=weblogic
    - konveyor.io/target=quarkus
```

### `mined-jndi-lookup-pattern` — high

**Detects JNDI lookup patterns using InitialContext**

> JNDI lookup patterns need to be replaced with CDI injection or MicroProfile REST Client in Quarkus

```yaml
- ruleID: mined-jndi-lookup-pattern
  description: Detects JNDI lookup patterns using InitialContext
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.naming.InitialContext
  message: |
    Replace JNDI lookups with CDI @Inject or MicroProfile REST Client for service access in Quarkus

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-persistence-context-producer` — high

**Detects @PersistenceContext EntityManager producer pattern**

> EntityManager injection pattern - @PersistenceContext producers are not needed in Quarkus as EntityManager can be injected directly

```yaml
- ruleID: mined-persistence-context-producer
  description: Detects @PersistenceContext EntityManager producer pattern
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.persistence.PersistenceContext
  message: |
    Remove @PersistenceContext producer methods - EntityManager can be injected directly with @Inject in Quarkus

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-quarkus-rest-client-dependency` — high

**Detects usage of deprecated quarkus-rest-client dependency**

> The quarkus-rest-client dependency was replaced with quarkus-resteasy-client in newer Quarkus versions, requiring dependency updates

```yaml
- ruleID: mined-quarkus-rest-client-dependency
  description: Detects usage of deprecated quarkus-rest-client dependency
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: pom.xml
      pattern: <artifactId>quarkus-rest-client</artifactId>
  message: |
    Replace quarkus-rest-client with quarkus-resteasy-client dependency. 
    The REST client implementation has been updated in newer Quarkus versions.

  labels:
    - konveyor.io/source=quarkus
    - konveyor.io/target=quarkus
```

### `mined-quarkus-rest-client-jackson-dependency` — high

**Detects usage of deprecated quarkus-rest-client-jackson dependency**

> The quarkus-rest-client-jackson dependency was replaced with quarkus-resteasy-client-jackson in newer Quarkus versions

```yaml
- ruleID: mined-quarkus-rest-client-jackson-dependency
  description: Detects usage of deprecated quarkus-rest-client-jackson dependency
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: pom.xml
      pattern: <artifactId>quarkus-rest-client-jackson</artifactId>
  message: |
    Replace quarkus-rest-client-jackson with quarkus-resteasy-client-jackson dependency.
    The REST client Jackson implementation has been updated in newer Quarkus versions.

  labels:
    - konveyor.io/source=quarkus
    - konveyor.io/target=quarkus
```

### `mined-quarkus-smallrye-reactive-messaging-dependency` — medium

**Detects usage of quarkus-smallrye-reactive-messaging dependency**

> The specific reactive messaging implementation was replaced with a more general quarkus-messaging dependency, though this may be project-specific

```yaml
- ruleID: mined-quarkus-smallrye-reactive-messaging-dependency
  description: Detects usage of quarkus-smallrye-reactive-messaging dependency
  category: optional
  effort: 5
  when:
    builtin.filecontent:
      filePattern: pom.xml
      pattern: <artifactId>quarkus-smallrye-reactive-messaging</artifactId>
  message: |
    Consider replacing quarkus-smallrye-reactive-messaging with quarkus-messaging dependency.
    The messaging implementation may have been simplified in newer Quarkus versions.

  labels:
    - konveyor.io/source=quarkus
    - konveyor.io/target=quarkus
```

### `mined-quarkus-maven-plugin-missing-goals` — medium

**Detects Quarkus Maven plugin configuration missing newer build goals**

> Additional build goals were added to the Quarkus Maven plugin for better code generation and native image support

```yaml
- ruleID: mined-quarkus-maven-plugin-missing-goals
  description: Detects Quarkus Maven plugin configuration missing newer build goals
  category: optional
  effort: 2
  when:
    builtin.filecontent:
      filePattern: pom.xml
      pattern:
        '<plugin>[\s\S]*?<groupId>.*quarkus.*</groupId>[\s\S]*?<artifactId>quarkus-maven-plugin</artifactId>[\s\S]*?<goal>build</goal>(?![\s\S]*?<goal>generate-code</goal>)

        '
  message: |
    Consider adding generate-code, generate-code-tests, and native-image-agent goals to the Quarkus Maven plugin.
    These goals provide better code generation and native compilation support in newer Quarkus versions.

  labels:
    - konveyor.io/source=quarkus
    - konveyor.io/target=quarkus
```

### `mined-javaee-beans-xml-webapp-location` — high

**Detects beans.xml file in webapp WEB-INF directory typical of Java EE applications**

> The beans.xml file in src/main/webapp/WEB-INF/ is a Java EE specific structure that needs to be moved or removed in Quarkus migration

```yaml
- ruleID: mined-javaee-beans-xml-webapp-location
  description: Detects beans.xml file in webapp WEB-INF directory typical of Java EE applications
  category: mandatory
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "**/src/main/webapp/WEB-INF/beans.xml"
  message: |
    This beans.xml file is located in the Java EE webapp structure. In Quarkus, beans.xml should be placed in src/main/resources/META-INF/ or can often be omitted entirely as Quarkus has CDI enabled by default.

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javaee-beans-xml-namespace` — high

**Detects Java EE beans.xml with javax namespace**

> The javax.jcp.org namespace in beans.xml is specific to Java EE and needs to be updated for Jakarta EE/Quarkus

```yaml
- ruleID: mined-javaee-beans-xml-namespace
  description: Detects Java EE beans.xml with javax namespace
  category: mandatory
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "**/beans.xml"
      pattern: xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  message: |
    This beans.xml uses the Java EE namespace. For Quarkus migration, update to use Jakarta EE namespace (https://jakarta.ee/xml/ns/jakartaee) or remove the file entirely as Quarkus enables CDI by default.

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javaee-persistence-xml-namespace` — high

**Detects Java EE persistence.xml with javax namespace**

> The javax.jcp.org namespace in persistence.xml is Java EE specific and needs to be updated or replaced with Quarkus configuration

```yaml
- ruleID: mined-javaee-persistence-xml-namespace
  description: Detects Java EE persistence.xml with javax namespace
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: "**/persistence.xml"
      pattern: xmlns="http://xmlns.jcp.org/xml/ns/persistence"
  message: |
    This persistence.xml uses Java EE namespace and configuration. In Quarkus, persistence configuration should be moved to application.properties using quarkus.datasource.* and quarkus.hibernate-orm.* properties.

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-jboss-datasource-jndi-lookup` — high

**Detects JBoss-specific JNDI datasource lookup pattern**

> JBoss-specific JNDI datasource references need to be replaced with Quarkus datasource configuration

```yaml
- ruleID: mined-jboss-datasource-jndi-lookup
  description: Detects JBoss-specific JNDI datasource lookup pattern
  category: mandatory
  effort: 4
  when:
    builtin.filecontent:
      filePattern: "**/persistence.xml"
      pattern: java:jboss/datasources/
  message: |
    This JBoss-specific JNDI datasource reference needs to be replaced. In Quarkus, configure datasource using quarkus.datasource.* properties in application.properties instead of JNDI lookups.

  labels:
    - konveyor.io/source=jboss-eap
    - konveyor.io/target=quarkus
```

### `mined-javaee-web-xml-webapp` — high

**Detects web.xml file in Java EE webapp structure**

> web.xml files are Java EE servlet container configuration that may need to be converted to Quarkus configuration or removed

```yaml
- ruleID: mined-javaee-web-xml-webapp
  description: Detects web.xml file in Java EE webapp structure
  category: optional
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "**/src/main/webapp/WEB-INF/web.xml"
  message: |
    This web.xml file contains Java EE servlet configuration. In Quarkus, most web.xml configuration can be replaced with application.properties settings or annotations. Review if this configuration is still needed.

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-javax-persistence-schema-generation-property` — high

**Detects javax.persistence schema generation properties**

> Java EE persistence properties using javax namespace need to be converted to Quarkus equivalents

```yaml
- ruleID: mined-javax-persistence-schema-generation-property
  description: Detects javax.persistence schema generation properties
  category: mandatory
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "**/persistence.xml"
      pattern: javax.persistence.schema-generation.database.action
  message: |
    This javax.persistence property should be replaced with Quarkus equivalent. Use quarkus.hibernate-orm.database.generation in application.properties instead.

  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus
```

### `mined-webapp-static-resources-location` — high

**Detects static web resources in traditional Java EE webapp directory structure**

> This is a fundamental structural change required when migrating from Java EE WAR packaging to Quarkus. The webapp directory structure is specific to traditional servlet containers and must be migrated to Quarkus's resource structure.

```yaml
- ruleID: mined-webapp-static-resources-location
  description: Detects static web resources in traditional Java EE webapp directory structure
  category: mandatory
  effort: 3
  when:
    builtin.file:
      pattern: src/main/webapp/*
  message: |
    Static web resources in src/main/webapp/ need to be moved to src/main/resources/META-INF/resources/ for Quarkus compatibility.

    In traditional Java EE applications, static resources (HTML, CSS, JS, images) are placed in src/main/webapp/.
    Quarkus follows a different convention where static resources should be placed in src/main/resources/META-INF/resources/.

    Migration steps:
    1. Create the directory src/main/resources/META-INF/resources/ if it doesn't exist
    2. Move all files from src/main/webapp/ to src/main/resources/META-INF/resources/
    3. Update any hardcoded references to the old paths in your application code
    4. Remove the empty src/main/webapp/ directory

  labels:
    - konveyor.io/source=eap7
    - konveyor.io/target=quarkus
```

### `mined-jsp-scriptlet-session-management` — high

**JSP scriptlet code using session management in HTML/JSP files**

> JSP scriptlets represent old Java EE web technology that needs to be replaced with modern approaches in Quarkus. Session management through JSP scriptlets is incompatible with Quarkus's approach.

```yaml
- ruleID: mined-jsp-scriptlet-session-management
  description: JSP scriptlet code using session management in HTML/JSP files
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: .*\.(jsp|html)$
      pattern: <%[^>]*request\.getSession\([^)]*\)[^>]*%>
  message: |
    JSP scriptlet session management detected. In Quarkus migration, replace JSP scriptlets with modern session management approaches using CDI beans, REST endpoints, or Quarkus session management extensions.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jsp-file-usage` — high

**JSP files that need to be migrated to modern templating or REST endpoints**

> JSP files are part of traditional Java EE web applications and need to be replaced with modern templating engines (like Qute) or REST endpoints in Quarkus migrations.

```yaml
- ruleID: mined-jsp-file-usage
  description: JSP files that need to be migrated to modern templating or REST endpoints
  category: mandatory
  effort: 5
  when:
    builtin.file:
      pattern: .*\.jsp$
  message: |
    JSP file detected. In Quarkus migration, JSP is not supported. Replace with Qute templating engine, REST endpoints returning JSON/HTML, or move static content to src/main/resources/META-INF/resources for static files.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

## Hints (0 generated, 0 skipped)
