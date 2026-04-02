# KAI Commit Miner Report

**Migration** (Inferred from manifest diffs): Migration from a Java EE 7 WAR-packaged monolithic application to Quarkus 3.12.3 framework. The migration involves replacing Java EE 7 APIs with Quarkus extensions, updating from Java 8 to Java 21, changing packaging from WAR to JAR, moving web resources from webapp to META-INF/resources, and adding Quarkus-specific plugins and dependencies including RESTEasy, Hibernate ORM, PostgreSQL JDBC, Flyway, and container image support.

**Source labels:** javaee, eap7, eap
**Target labels:** quarkus, quarkus3, jakarta-ee, cloud-readiness, eap8, eap

**Label selector:** `konveyor.io/target=quarkus || konveyor.io/target=quarkus3 || konveyor.io/target=jakarta-ee || konveyor.io/target=cloud-readiness || konveyor.io/target=eap8 || konveyor.io/target=eap`

## Summary

| Metric               | Count |
| -------------------- | ----- |
| Violations resolved  | 0     |
| Files changed        | 2558  |
| Violation types      | 0     |
| Hints generated      | 0     |
| Hints skipped        | 0     |
| New rules discovered | 15    |

## New Rule Candidates (15)

Proposed analyzer-lsp rules detecting pre-migration patterns. 15 high-relevance, 0 lower.

### `mined-javax-persistence-to-jakarta` — high

**Detect javax.persistence imports that need migration to jakarta.persistence**

> Direct import migration from javax to jakarta namespace is a core requirement for Java EE to Jakarta EE/Quarkus migration

```yaml
- ruleID: mined-javax-persistence-to-jakarta
  description: Detect javax.persistence imports that need migration to jakarta.persistence
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.persistence.*
  message: |
    Replace javax.persistence imports with jakarta.persistence imports for Jakarta EE compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-enterprise-to-jakarta` — high

**Detect javax.enterprise imports that need migration to jakarta.enterprise**

> CDI namespace migration from javax to jakarta is required for Quarkus compatibility

```yaml
- ruleID: mined-javax-enterprise-to-jakarta
  description: Detect javax.enterprise imports that need migration to jakarta.enterprise
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.enterprise.*
  message: |
    Replace javax.enterprise imports with jakarta.enterprise imports for CDI compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-inject-to-jakarta` — high

**Detect javax.inject imports that need migration to jakarta.inject**

> Dependency injection namespace migration from javax to jakarta is required for Quarkus

```yaml
- ruleID: mined-javax-inject-to-jakarta
  description: Detect javax.inject imports that need migration to jakarta.inject
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.inject.*
  message: |
    Replace javax.inject imports with jakarta.inject imports for dependency injection compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-ws-rs-to-jakarta` — high

**Detect javax.ws.rs imports that need migration to jakarta.ws.rs**

> JAX-RS namespace migration from javax to jakarta is required for REST services in Quarkus

```yaml
- ruleID: mined-javax-ws-rs-to-jakarta
  description: Detect javax.ws.rs imports that need migration to jakarta.ws.rs
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.ws.rs.*
  message: |
    Replace javax.ws.rs imports with jakarta.ws.rs imports for JAX-RS compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-xml-bind-to-jakarta` — high

**Detect javax.xml.bind imports that need migration to jakarta.xml.bind**

> JAXB namespace migration from javax to jakarta is required for XML binding in Quarkus

```yaml
- ruleID: mined-javax-xml-bind-to-jakarta
  description: Detect javax.xml.bind imports that need migration to jakarta.xml.bind
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.xml.bind.*
  message: |
    Replace javax.xml.bind imports with jakarta.xml.bind imports for JAXB compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-javax-json-to-jakarta` — high

**Detect javax.json imports that need migration to jakarta.json**

> JSON-P namespace migration from javax to jakarta is required for JSON processing in Quarkus

```yaml
- ruleID: mined-javax-json-to-jakarta
  description: Detect javax.json imports that need migration to jakarta.json
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: javax.json.*
  message: |
    Replace javax.json imports with jakarta.json imports for JSON-P compatibility in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-stateless-annotation` — high

**Detect @Stateless EJB annotation that needs migration to @ApplicationScoped**

> EJB @Stateless beans need to be converted to CDI @ApplicationScoped beans in Quarkus as EJBs are not supported

```yaml
- ruleID: mined-ejb-stateless-annotation
  description: Detect @Stateless EJB annotation that needs migration to @ApplicationScoped
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Stateless
  message: |
    Replace @Stateless EJB annotation with @ApplicationScoped CDI annotation. Quarkus uses CDI instead of EJBs for dependency injection and lifecycle management.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-stateful-annotation` — high

**Detect @Stateful EJB annotation that needs migration to @SessionScoped**

> EJB @Stateful beans need to be converted to CDI @SessionScoped beans in Quarkus as EJBs are not supported

```yaml
- ruleID: mined-ejb-stateful-annotation
  description: Detect @Stateful EJB annotation that needs migration to @SessionScoped
  category: mandatory
  effort: 3
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Stateful
  message: |
    Replace @Stateful EJB annotation with @SessionScoped CDI annotation. Quarkus uses CDI scopes instead of EJBs for stateful components.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-message-driven-bean` — high

**Detect @MessageDriven EJB annotation that needs migration to reactive messaging**

> Message-driven beans need to be replaced with Quarkus reactive messaging using @Incoming annotations

```yaml
- ruleID: mined-message-driven-bean
  description: Detect @MessageDriven EJB annotation that needs migration to reactive messaging
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.MessageDriven
  message: |
    Replace @MessageDriven EJB with Quarkus reactive messaging using @Incoming annotation and MicroProfile Reactive Messaging

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-jms-message-listener` — high

**Detect JMS MessageListener interface that needs migration to reactive messaging**

> JMS MessageListener needs to be replaced with Quarkus reactive messaging pattern for message processing

```yaml
- ruleID: mined-jms-message-listener
  description: Detect JMS MessageListener interface that needs migration to reactive messaging
  category: mandatory
  effort: 5
  when:
    java.referenced:
      location: TYPE
      pattern: javax.jms.MessageListener
  message: |
    Replace JMS MessageListener with Quarkus reactive messaging using @Incoming methods and MicroProfile Reactive Messaging

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-persistence-context-annotation` — high

**Detect @PersistenceContext annotation that needs migration to @Inject EntityManager**

> JPA @PersistenceContext needs to be replaced with CDI @Inject for EntityManager injection in Quarkus

```yaml
- ruleID: mined-persistence-context-annotation
  description: Detect @PersistenceContext annotation that needs migration to @Inject EntityManager
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.persistence.PersistenceContext
  message: |
    Replace @PersistenceContext with @Inject for EntityManager injection in Quarkus. Remove the Resources producer class and inject EntityManager directly.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-resource-annotation-jndi` — high

**Detect @Resource annotation with JNDI lookup that needs migration**

> JNDI resource lookups need to be replaced with CDI injection or configuration properties in Quarkus

```yaml
- ruleID: mined-resource-annotation-jndi
  description: Detect @Resource annotation with JNDI lookup that needs migration
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.annotation.Resource
  message: |
    Replace @Resource JNDI lookups with CDI @Inject or Quarkus configuration properties. JNDI is not available in Quarkus.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-ejb-remote-interface` — high

**Detect @Remote EJB annotation that needs migration to REST client**

> EJB remote interfaces need to be replaced with REST clients in Quarkus microservices architecture

```yaml
- ruleID: mined-ejb-remote-interface
  description: Detect @Remote EJB annotation that needs migration to REST client
  category: mandatory
  effort: 4
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Remote
  message: |
    Replace @Remote EJB interface with MicroProfile REST Client using @RegisterRestClient for service communication in Quarkus

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-startup-singleton-ejb` — high

**Detect @Startup @Singleton EJB pattern that needs migration to Quarkus startup**

> EJB startup singletons need to be converted to Quarkus startup beans with @Singleton and io.quarkus.runtime.Startup

```yaml
- ruleID: mined-startup-singleton-ejb
  description: Detect @Startup @Singleton EJB pattern that needs migration to Quarkus startup
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.Startup
  message: |
    Replace EJB @Startup with io.quarkus.runtime.Startup and use jakarta.inject.Singleton instead of javax.ejb.Singleton

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

### `mined-transaction-management` — high

**Detect @TransactionManagement annotation that is not needed in Quarkus**

> EJB transaction management annotations are not needed in Quarkus as it uses different transaction handling

```yaml
- ruleID: mined-transaction-management
  description: Detect @TransactionManagement annotation that is not needed in Quarkus
  category: optional
  effort: 1
  when:
    java.referenced:
      location: ANNOTATION
      pattern: javax.ejb.TransactionManagement
  message: |
    Remove @TransactionManagement annotation. Quarkus handles transactions automatically or use @Transactional for declarative transaction management.

  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```

## Hints (0 generated, 0 skipped)
