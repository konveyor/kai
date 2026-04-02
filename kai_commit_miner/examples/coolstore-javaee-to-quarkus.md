# KAI Commit Miner Report

**Migration** (Inferred from manifest diffs): Migration from Java EE 7 monolithic application to Quarkus 3.12.3 framework. The application is being transformed from a traditional WAR-packaged Java EE application using JavaEE Web API 7.0 to a modern cloud-native Quarkus application. Key changes include replacing Java EE dependencies with Quarkus extensions (quarkus-arc, quarkus-resteasy, quarkus-hibernate-orm, quarkus-flyway), updating from Java 8 to Java 21, changing packaging from WAR to JAR, moving static web resources from webapp to META-INF/resources directory structure, and adding native compilation support with GraalVM.

**Source labels:** java-ee, eap7, hibernate5.0
**Target labels:** quarkus, quarkus3, jakarta-ee, jakarta-ee9, cloud-readiness, hibernate, hibernate6, resteasy, openjdk21

**Label selector:** `konveyor.io/target=quarkus || konveyor.io/target=quarkus3 || konveyor.io/target=jakarta-ee || konveyor.io/target=jakarta-ee9 || konveyor.io/target=cloud-readiness || konveyor.io/target=hibernate || konveyor.io/target=hibernate6 || konveyor.io/target=resteasy || konveyor.io/target=openjdk21`

## Summary

| Metric               | Count |
| -------------------- | ----- |
| Violations resolved  | 204   |
| Files changed        | 2558  |
| Violation types      | 34    |
| Hints generated      | 34    |
| Hints skipped        | 8     |
| New rules discovered | 7     |

## New Rule Candidates (7)

Proposed analyzer-lsp rules detecting pre-migration patterns. 7 high-relevance, 0 lower.

### `mined-webapp-to-meta-inf-resources` — high

**Detects webapp directory structure that needs migration to META-INF/resources**

> Static web resources must be moved from src/main/webapp to src/main/resources/META-INF/resources in Quarkus, as Quarkus doesn't use traditional WAR packaging

```yaml
- ruleID: mined-webapp-to-meta-inf-resources
  description: Detects webapp directory structure that needs migration to META-INF/resources
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: src/main/webapp/**
  message: |
    Move static web resources from src/main/webapp to src/main/resources/META-INF/resources directory.
    Quarkus serves static content from META-INF/resources instead of the traditional webapp directory.

  labels:
    - konveyor.io/source=javaee7
    - konveyor.io/target=quarkus
```

### `mined-beans-xml-removal` — high

**Detects beans.xml file that may not be needed in Quarkus**

> Quarkus has different CDI discovery mechanisms and beans.xml may not be required, especially with bean-discovery-mode="all"

```yaml
- ruleID: mined-beans-xml-removal
  description: Detects beans.xml file that may not be needed in Quarkus
  category: optional
  effort: 1
  when:
    builtin.filecontent:
      filePattern: "**/beans.xml"
      pattern: bean-discovery-mode="all"
  message: |
    Consider removing beans.xml or updating CDI configuration for Quarkus.
    Quarkus uses different CDI discovery mechanisms and may not require beans.xml with bean-discovery-mode="all".

  labels:
    - konveyor.io/source=javaee7
    - konveyor.io/target=quarkus
```

### `mined-web-xml-removal` — high

**Detects web.xml file that is not used in Quarkus**

> Quarkus doesn't use web.xml as it's not a traditional servlet container deployment

```yaml
- ruleID: mined-web-xml-removal
  description: Detects web.xml file that is not used in Quarkus
  category: mandatory
  effort: 2
  when:
    builtin.filecontent:
      filePattern: "**/web.xml"
      pattern: <web-app
  message: |
    Remove web.xml file. Quarkus doesn't use traditional web.xml deployment descriptors.
    Configure web settings through application.properties or annotations instead.

  labels:
    - konveyor.io/source=javaee7
    - konveyor.io/target=quarkus
```

### `mined-jsp-scriptlet-removal` — high

**Detects JSP scriptlets that need to be removed for Quarkus**

> JSP scriptlets with session management code need to be replaced with modern approaches as Quarkus doesn't support JSP

```yaml
- ruleID: mined-jsp-scriptlet-removal
  description: Detects JSP scriptlets that need to be removed for Quarkus
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: "*.jsp"
      pattern: request.getSession(true)
  message: |
    Remove JSP scriptlets and migrate to a modern web framework.
    Quarkus doesn't support JSP. Consider using Qute templates or a frontend framework.

  labels:
    - konveyor.io/source=javaee7
    - konveyor.io/target=quarkus
```

### `mined-persistence-xml-removal` — high

**Detects persistence.xml that should be migrated to Quarkus configuration**

> Quarkus uses application.properties for database configuration instead of persistence.xml

```yaml
- ruleID: mined-persistence-xml-removal
  description: Detects persistence.xml that should be migrated to Quarkus configuration
  category: mandatory
  effort: 3
  when:
    builtin.filecontent:
      filePattern: "**/persistence.xml"
      pattern: <persistence-unit
  message: |
    Remove persistence.xml and configure database settings in application.properties.
    Use properties like quarkus.datasource.db-kind, quarkus.hibernate-orm.database.generation, etc.

  labels:
    - konveyor.io/source=javaee7
    - konveyor.io/target=quarkus
```

### `mined-weblogic-stubs-removal` — high

**Detects WebLogic-specific stub classes that should be removed**

> WebLogic-specific classes like ApplicationLifecycleListener need to be removed and replaced with Quarkus equivalents

```yaml
- ruleID: mined-weblogic-stubs-removal
  description: Detects WebLogic-specific stub classes that should be removed
  category: mandatory
  effort: 2
  when:
    java.referenced:
      location: TYPE
      pattern: weblogic.application.ApplicationLifecycleListener
  message: |
    Remove WebLogic-specific ApplicationLifecycleListener.
    Use Quarkus startup/shutdown events with @Observes StartupEvent/@Observes ShutdownEvent instead.

  labels:
    - konveyor.io/source=javaee7+weblogic
    - konveyor.io/target=quarkus
```

### `mined-weblogic-logging-removal` — high

**Detects WebLogic-specific logging classes that should be replaced**

> WebLogic NonCatalogLogger should be replaced with standard logging frameworks supported by Quarkus

```yaml
- ruleID: mined-weblogic-logging-removal
  description: Detects WebLogic-specific logging classes that should be replaced
  category: mandatory
  effort: 1
  when:
    java.referenced:
      location: IMPORT
      pattern: weblogic.i18n.logging.NonCatalogLogger
  message: |
    Replace WebLogic NonCatalogLogger with standard logging.
    Use JBoss Logging (io.quarkus.logging.Log) or java.util.logging.Logger instead.

  labels:
    - konveyor.io/source=javaee7+weblogic
    - konveyor.io/target=quarkus
```

## Hints (34 generated, 8 skipped)

### cloud-readiness / session-00000

_1 incidents, 0 skipped_

GOTCHAS:

- Simply removing <distributable/> without addressing session state will break user experience
- Quarkus native mode doesn't support traditional HTTP session replication at all

ACCOMPANYING CHANGES:

- Remove <distributable/> tag from web.xml entirely
- Add quarkus-redis-client or quarkus-infinispan-client dependency if implementing external session store
- Configure application.properties with cache/redis connection settings if using external store
- Update session handling code to use stateless patterns or explicit cache operations
- Consider adding quarkus-oidc or quarkus-security-jwt for token-based authentication instead of sessions

ORDERING: Remove distributable configuration before packaging changes, as Quarkus JAR packaging doesn't support traditional session replication

### eap7/weblogic/tests/data / hibernate4-00039

_4 incidents, 1 skipped_

<details><summary>Skipped: rule description is sufficient

The examples show only import changes from `java</summary>

rule description is sufficient

The examples show only import changes from `javax.persistence.*` to `jakarta.persistence.*`, which is a standard part of the Java EE to Jakarta EE migration that would be covered by other rules. The hibernate4-00039 rule is specifically about Oracle dialect byte array mapping behavior, and the rule description already provides complete information about the configuration option (`hibernate.dialect.oracle.prefer_longvarbinary`) needed to maintain backward compatibility if desired.

</details>

### eap8/eap7 / hibernate-00005

_2 incidents, 0 skipped_

GOTCHAS: The rule focuses on sequence naming changes but doesn't mention that the primary issue triggering this violation is often the use of old javax.persistence imports instead of jakarta.persistence imports.

ACCOMPANYING CHANGES:

- Replace all javax.persistence imports with jakarta.persistence imports in the same file
- Update any other javax._ imports to their jakarta._ equivalents if present
- Ensure pom.xml/build.gradle has quarkus-hibernate-orm extension instead of Java EE persistence dependencies

ORDERING: Import changes must be done before addressing the actual sequence naming strategy, as Quarkus requires Jakarta EE APIs.

<details><summary><code>src/main/java/com/redhat/coolstore/model/Order.java</code></summary>

Before:

```
import javax.persistence.Table;

@Entity
@Table(name = "ORDERS")
public class Order implements Serializable {

	private static final long serialVersionUID = -1L;

	@Id
	@GeneratedValue
	private long orderId;

	private String customerName;

	private String customerEmail;

	private double orderValue;

```

After:

```
import jakarta.persistence.Table;

@Entity
@Table(name = "ORDERS")
public class Order implements Serializable {

	private static final long serialVersionUID = -1L;

	@Id
	@GeneratedValue
	private long orderId;

	private String customerName;

	private String customerEmail;

	private double orderValue
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/model/OrderItem.java</code></summary>

Before:

```
import javax.persistence.Table;

@Entity
@Table(name = "ORDER_ITEMS")
public class OrderItem implements Serializable {
	private static final long serialVersionUID = 64565445665456666L;

	@Id
	@Column(name="ID")
	@GeneratedValue
	private long id;

	private int quantity;

	private String productId;


```

After:

```
import jakarta.persistence.Table;

@Entity
@Table(name = "ORDER_ITEMS")
public class OrderItem implements Serializable {
	private static final long serialVersionUID = 64565445665456666L;

	@Id
	@Column(name="ID")
	@GeneratedValue
	private long id;

	private int quantity;

	private String productId;

```

</details>

### eap8/eap7 / javaee-to-jakarta-namespaces-00001

_3 incidents, 0 skipped_

GOTCHAS: In Quarkus migration, beans.xml files may be auto-generated or managed by the framework - direct edits might be overwritten during build.

ACCOMPANYING CHANGES:

- Update Maven/Gradle dependencies to use Jakarta EE versions (jakarta.enterprise:jakarta.enterprise.cdi-api instead of javax.enterprise:cdi-api)
- Move beans.xml from src/main/webapp/WEB-INF/ to src/main/resources/META-INF/ for JAR packaging
- Verify quarkus-arc extension is included in pom.xml/build.gradle as it handles CDI in Quarkus

ORDERING: Update dependencies first, then let Quarkus generate correct beans.xml, or manually update after dependency changes are complete.

### eap8/eap7 / javaee-to-jakarta-namespaces-00002

_3 incidents, 0 skipped_

GOTCHAS:

- Don't mix Java EE and Jakarta namespaces in the same persistence.xml - all namespace references must be updated together
- Version attribute must match the Jakarta specification version (3.0 or higher), not just the namespace

ACCOMPANYING CHANGES:

- Update Maven/Gradle dependencies from javax.persistence to jakarta.persistence artifacts
- Add quarkus-hibernate-orm extension dependency
- May need to update persistence-unit configuration properties for Quarkus-specific settings
- Verify datasource configuration matches Quarkus format in application.properties

ORDERING: Update dependencies first, then namespace changes, as the new Jakarta artifacts are required for the updated schema validation

### eap8/eap7 / javaee-to-jakarta-namespaces-00006

_1 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Move beans.xml from src/main/webapp/WEB-INF/ to src/main/resources/META-INF/ (Quarkus uses JAR packaging, not WAR)
- Update pom.xml packaging from <packaging>war</packaging> to <packaging>jar</packaging>
- Add quarkus-arc dependency if not already present for CDI support

ORDERING: Move file location before updating XSD references to avoid build errors

### eap8/eap7 / javaee-to-jakarta-namespaces-00030

_1 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Update Maven/Gradle dependencies to use Jakarta Persistence API instead of Java EE JPA dependencies
- Verify Quarkus Hibernate ORM extension is configured (quarkus-hibernate-orm) as it provides Jakarta Persistence implementation
- Check that persistence unit configuration in application.properties aligns with Jakarta Persistence 3.0 requirements

ORDERING: Update dependencies before modifying XSD references to ensure proper validation during build

### eap8/eap7 / javaee-to-jakarta-namespaces-00033

_1 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Update Maven/Gradle dependencies to use Jakarta EE specifications instead of Java EE versions
- Verify that persistence provider configuration in the same file is compatible with the new Jakarta version
- Check that any referenced entity classes use Jakarta namespace imports (@Entity, @Id, etc.)

ORDERING: Update dependencies in pom.xml/build.gradle before fixing persistence.xml version attributes to avoid runtime conflicts

### eap8/eap7 / javax-to-jakarta-import-00001

_98 incidents, 6 skipped_

<details><summary>Skipped: rule description is sufficient</summary>

rule description is sufficient

</details>

GOTCHAS:

- IDE auto-import may still suggest javax packages - verify all imports are updated
- Mixed javax/jakarta imports in same file will cause compilation errors

ACCOMPANYING CHANGES:

- Update pom.xml dependencies from javax._ to jakarta._ artifacts (e.g., javax.persistence-api → jakarta.persistence-api)
- Check for javax package references in configuration files (persistence.xml, web.xml)
- Update any string literals or reflection code that reference javax package names

ORDERING: Update Maven dependencies before fixing imports to ensure jakarta packages are available on classpath

<details><summary><code>src/main/java/com/redhat/coolstore/model/InventoryEntity.java</code></summary>

Before:

```
package com.redhat.coolstore.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@XmlR
```

After:

```
package com.redhat.coolstore.model;

import java.io.Serializable;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.xml.bind.annotation.XmlRootElement;

@
```

</details>

<details><summary>Skipped: The existing hint already comprehensively covers the key patterns shown in the e</summary>

The existing hint already comprehensively covers the key patterns shown in the examples - the import replacements from javax to jakarta, the dependency updates needed in pom.xml, configuration file updates, and the proper ordering of making dependency changes before import fixes. The examples show straightforward import replacements that are already addressed by the existing hint.

</details>

<details><summary>Skipped: The previously generated hint already covers the key patterns seen in these exam</summary>

The previously generated hint already covers the key patterns seen in these examples. The examples show standard javax→jakarta import replacements that are well-covered by the existing hint's guidance on updating dependencies, checking configuration files, and handling mixed imports. The architectural changes (EJB→CDI, JMS→reactive messaging) are separate migration concerns beyond the scope of this specific import replacement rule.

</details>

<details><summary>Skipped: The previously generated hint already comprehensively covers all the key pattern</summary>

The previously generated hint already comprehensively covers all the key patterns from the examples. The examples show straightforward javax→jakarta import replacements, which are already covered by the existing hint's guidance on IDE auto-import gotchas, mixed import compilation errors, dependency updates, configuration file updates, and proper ordering of Maven changes before import fixes.

</details>

GOTCHAS:

- Simply replacing javax with jakarta imports may not be sufficient - code often needs architectural changes (EJB → CDI, JMS → reactive messaging)
- IDE auto-import may still suggest javax packages - verify all imports are updated
- Mixed javax/jakarta imports in same file will cause compilation errors

ACCOMPANYING CHANGES:

- Replace EJB annotations (@Stateless, @Stateful, @MessageDriven) with CDI equivalents (@ApplicationScoped, @SessionScoped)
- Convert JMS MessageListener pattern to MicroProfile Reactive Messaging (@Incoming)
- Replace EJB remote interfaces with REST clients (@RestClient) or direct injection
- Remove JNDI lookup code and replace with CDI injection
- Update method signatures when moving from interface implementations to direct services
- Add new imports for Quarkus/MicroProfile APIs (reactive messaging, REST client)
- Update pom.xml dependencies from javax._ to jakarta._ artifacts

ORDERING: Update Maven dependencies and add Quarkus extensions before fixing imports to ensure jakarta packages and new APIs are available on classpath

<details><summary><code>src/main/java/com/redhat/coolstore/service/CatalogService.java</code></summary>

Before:

```
import java.util.List;
import java.util.logging.Logger;

import javax.inject.Inject;

import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;

impo
```

After:

```
import java.util.List;
import java.util.logging.Logger;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;

import jakar
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderService.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import com.redhat.coolstore.model.Order;
import java.util.List;
import javax.ejb.Stateless;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
i
```

After:

```
package com.redhat.coolstore.service;

import com.redhat.coolstore.model.Order;
import java.util.List;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.per
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import javax.ejb.ActivationConfigProperty;
import javax.ejb.MessageDriven;
import javax.inject.Inject;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Or
```

After:

```
package com.redhat.coolstore.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.util
```

</details>

<details><summary>Skipped: The existing hint already comprehensively covers all the patterns shown in these</summary>

The existing hint already comprehensively covers all the patterns shown in these examples, including the conversion of JMS MessageListener to MicroProfile Reactive Messaging with @Incoming annotation, replacement of @MessageDriven with @ApplicationScoped, addition of @Blocking and @Transactional annotations, simplification of message handling from JMS Message objects to direct String parameters, and removal of JNDI lookup code. The examples don't reveal any new patterns beyond what's already documented in the hint.

</details>

GOTCHAS:

- DataSource injection changes from @Resource JNDI lookup to direct @Inject - may require datasource configuration updates
- JMS patterns require complete architectural shift to reactive messaging, not just import changes
- Method visibility may need adjustment (private @PostConstruct methods should become package-private in Quarkus)

ACCOMPANYING CHANGES:

- Replace @Stateless/@Singleton EJB with @RequestScoped/@Singleton CDI scopes
- Remove @TransactionManagement annotations (Quarkus handles transactions automatically)
- Convert @Resource JNDI lookups to @Inject for DataSource and other resources
- Replace JMS (@Resource Topic, JMSContext) with MicroProfile Reactive Messaging (@Channel, Emitter)
- Add Quarkus-specific imports (io.quarkus.runtime.Startup, @Broadcast annotation)
- Update Flyway API calls from deprecated setters to builder pattern
- Change @PostConstruct method visibility from private to package-private or public

ORDERING: Add quarkus-smallrye-reactive-messaging extension to pom.xml before converting JMS code to ensure reactive messaging APIs are available

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import java.util.logging.Logger;
import javax.ejb.Stateless;
import javax.annotation.Resource;
import javax.inject.Inject;
import javax.jms.JMSContext;
import javax.jms.Topic;

import com.redhat.coolstore.model.ShoppingCart;
import com.redhat.coolstore.utils.Tr
```

After:

```
package com.redhat.coolstore.service;

import java.util.logging.Logger;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;

import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;

import com.redhat.coolstore
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java</code></summary>

Before:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import javax.ejb.TransactionManagement;
import javax.ejb
```

After:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import io.quarkus.runtime.Startup;
import jakarta.annotation.PostConstruct;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;

import javax.sql.DataSource;
import java.ut
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java</code></summary>

Before:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import javax.ejb.TransactionManagement;
import javax.ejb
```

After:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import io.quarkus.runtime.Startup;
import jakarta.annotation.PostConstruct;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;

import javax.sql.DataSource;
import java.ut
```

</details>

<details><summary>Skipped: The examples show straightforward javax.json to jakarta.json import replacements</summary>

The examples show straightforward javax.json to jakarta.json import replacements with no additional complexities. The rule description and incident message already provide sufficient guidance for this simple import substitution pattern. The previously generated hint already covers the more complex patterns that require additional considerations.

</details>

### eap8/eap7 / javax-to-jakarta-properties-00001

_1 incidents, 0 skipped_

GOTCHAS: Properties may be referenced in multiple configuration files (persistence.xml, web.xml, application.properties) - ensure all references are updated consistently

ACCOMPANYING CHANGES:

- Update Maven/Gradle dependencies from javax._ to jakarta._ packages
- Verify property validation still works after namespace change
- Check that application servers/containers support the jakarta namespace versions

ORDERING: Update dependencies before changing property references to avoid runtime errors

### openjdk11/openjdk8 / removed-javaee-modules-00010

_1 incidents, 0 skipped_

GOTCHAS:

- CORBA removal often appears in messaging/remote communication code that needs architectural changes, not just dependency swaps
- PortableRemoteObject.narrow() calls indicate CORBA usage that requires complete messaging pattern replacement

ACCOMPANYING CHANGES:

- Replace Java EE messaging (JMS MessageListener) with MicroProfile Reactive Messaging (@Incoming)
- Remove JNDI lookup code and manual connection management
- Add @Blocking and @Transactional annotations for synchronous processing
- Update imports from javax._ to jakarta._ and add io.smallrye.\* imports
- Simplify method signatures (Message parameter becomes direct String/object type)
- Remove init()/close() lifecycle methods - Quarkus handles connection management

ORDERING: Must happen after Quarkus messaging extensions are added to dependencies and messaging configuration is updated in application.properties

<details><summary><code>src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java</code></summary>

Before:

```

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import javax.inject.Inject;
import javax.jms.*;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.rmi.PortableRemoteObject;
import java.util.Has
```

After:

```

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.Incoming;

public class InventoryNotif
```

</details>

### openjdk11/openjdk8 / removed-javaee-modules-00020

_3 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Replace javax.inject imports with jakarta.inject equivalents (Inject, Singleton)
- Update EJB annotations to Quarkus equivalents (@Singleton @Startup -> jakarta.inject.Singleton + io.quarkus.runtime.Startup)
- Remove EJB-specific annotations like @TransactionManagement, @Stateless, @Resource
- Replace @Resource DataSource injection with @Inject
- Update JMS messaging patterns to MicroProfile Reactive Messaging (@Channel, Emitter)
- Change method visibility from private to package-private for @PostConstruct methods in Quarkus

GOTCHAS:

- @PostConstruct methods must not be private in Quarkus (CDI requirement)
- @Resource(mappedName/lookup) becomes @Inject with datasource configuration in application.properties

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import java.util.logging.Logger;
import javax.ejb.Stateless;
import javax.annotation.Resource;
import javax.inject.Inject;
import javax.jms.JMSContext;
import javax.jms.Topic;

import com.redhat.coolstore.model.ShoppingCart;
import com.redhat.coolstore.utils.Tr
```

After:

```
package com.redhat.coolstore.service;

import java.util.logging.Logger;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;

import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;

import com.redhat.coolstore
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java</code></summary>

Before:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import javax.ejb.TransactionManagement;
import javax.ejb
```

After:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import io.quarkus.runtime.Startup;
import jakarta.annotation.PostConstruct;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;

import javax.sql.DataSource;
import java.ut
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java</code></summary>

Before:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import javax.ejb.TransactionManagement;
import javax.ejb
```

After:

```
package com.redhat.coolstore.utils;

import org.flywaydb.core.Flyway;
import org.flywaydb.core.api.FlywayException;

import io.quarkus.runtime.Startup;
import jakarta.annotation.PostConstruct;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;

import javax.sql.DataSource;
import java.ut
```

</details>

### openjdk7/oraclejdk7 / oracle2openjdk-00006

_1 incidents, 1 skipped_

<details><summary>Skipped: rule description is sufficient

The provided example shows a different rule viol</summary>

rule description is sufficient

The provided example shows a different rule violation (javax.ws.rs to jakarta.ws.rs migration) than the oracle2openjdk-00006 rule which is about JPEG image encoder/decoder usage. The rule description already clearly states to replace `com.sun.image.codec.jpeg` package usage with `javax.imageio.ImageIO`, which is straightforward API replacement that doesn't require additional context about gotchas, ordering, or accompanying changes beyond the obvious import changes.

</details>

### quarkus/springboot / cdi-to-quarkus-00030

_1 incidents, 0 skipped_

GOTCHAS: Don't just delete beans.xml - check if it contains custom interceptor, decorator, or alternative configurations that need migration to Quarkus-specific approaches

ACCOMPANYING CHANGES:

- Move beans.xml from src/main/webapp/WEB-INF/ to src/main/resources/META-INF/ if keeping minimal version
- Replace <interceptors> declarations with @Priority annotations on interceptor classes
- Replace <decorators> with Quarkus-compatible decorator patterns
- Replace <alternatives> with @QuarkusTest alternatives or application.properties config
- Update CDI scope annotations to use jakarta.enterprise.context instead of javax.enterprise.context if not already done

ORDERING: Handle after updating CDI annotations and dependencies, before final packaging changes

### quarkus/springboot / cdi-to-quarkus-00040

_2 incidents, 0 skipped_

GOTCHAS: Removing @Produces may break injection if the producer method provides complex logic or transformations - only remove when it's a simple getter/accessor pattern.

ACCOMPANYING CHANGES:

- Update imports from javax.enterprise.inject.Produces to jakarta.enterprise.inject.Produces if keeping @Produces
- May need to remove entire producer classes if they only contained simple EntityManager producers (Quarkus can inject EntityManager directly)
- Ensure @PersistenceContext fields have proper injection alternatives in Quarkus (often just @Inject EntityManager)

ORDERING: Handle after updating all javax._ to jakarta._ imports but before testing injection points.

<details><summary><code>src/main/java/com/redhat/coolstore/persistence/Resources.java</code></summary>

Before:

```
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Dependent
public class Resources {

    @PersistenceContext
    private EntityManager em;

    @Produces
    public EntityManager getEntityManager() {
        return em;
    }
}

```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/utils/Producers.java</code></summary>

Before:

```
import javax.enterprise.inject.Produces;
import javax.enterprise.inject.spi.InjectionPoint;
import java.util.logging.Logger;


public class Producers {

    Logger log = Logger.getLogger(Producers.class.getName());

    @Produces
    public Logger produceLog(InjectionPoint injectionPoint) {

```

After:

```
import jakarta.enterprise.inject.Produces;
import jakarta.enterprise.inject.spi.InjectionPoint;
import java.util.logging.Logger;


public class Producers {

    Logger log = Logger.getLogger(Producers.class.getName());

    @Produces
    public Logger produceLog(InjectionPoint injectionPoint) {

```

</details>

### quarkus/springboot / ee-to-quarkus-00000

_5 incidents, 0 skipped_

GOTCHAS:

- Not all @Stateless beans should become CDI beans - some may need to be converted to REST endpoints (@Path) instead
- @Remote interface implementations should be removed entirely, not just replaced with CDI scopes

ACCOMPANYING CHANGES:

- Remove @Remote annotation and interface implementation when present
- Update all javax._ imports to jakarta._ equivalents (javax.inject, javax.persistence, javax.ejb, javax.annotation)
- Consider converting to REST endpoints with @Path/@POST instead of CDI beans for service boundaries
- May need to replace JMS/EJB messaging patterns with MicroProfile Reactive Messaging (@Channel, Emitter)
- Remove @Override annotations when no longer implementing interfaces

ORDERING: Import updates (javax to jakarta) should be done alongside the @Stateless replacement to avoid compilation errors

<details><summary><code>src/main/java/com/redhat/coolstore/service/CatalogService.java</code></summary>

Before:

```
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@Stateless
public class CatalogService {

    @Injec
```

After:

```

import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;

import jakarta.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@ApplicationScoped
public class CatalogService {

    @Inject
    Logge
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderService.java</code></summary>

Before:

```
import com.redhat.coolstore.model.Order;
import java.util.List;
import javax.ejb.Stateless;
import javax.inject.Inject;
import javax.persistence.EntityManager;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

```

After:

```
import com.redhat.coolstore.model.Order;
import java.util.List;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/ProductService.java</code></summary>

Before:

```
import com.redhat.coolstore.utils.Transformers;

import javax.ejb.Stateless;
import javax.inject.Inject;
import java.util.List;
import java.util.stream.Collectors;

import static com.redhat.coolstore.utils.Transformers.toProduct;

@Stateless
public class ProductService {

    @Inject
    CatalogServ
```

After:

```
import com.redhat.coolstore.utils.Transformers;

import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import java.util.List;
import java.util.stream.Collectors;

import static com.redhat.coolstore.utils.Transformers.toProduct;

@RequestScoped
public class ProductService {


```

</details>

### quarkus/springboot / ee-to-quarkus-00010

_1 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Update imports from javax._ to jakarta._ packages (javax.ejb.Stateful → jakarta.enterprise.context.SessionScoped)
- Replace JNDI lookup patterns with CDI @Inject and @RestClient annotations for service dependencies
- Remove manual JNDI lookup methods and related javax.naming imports
- Add MicroProfile REST Client dependencies for external service calls

GOTCHAS:

- @SessionScoped requires quarkus-undertow extension activation
- JNDI-based service lookups must be replaced with CDI injection patterns, not just annotation swapping

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartService.java</code></summary>

Before:

```
import javax.inject.Inject;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

import com.redhat.coolstore.model.Product;
import com.redhat.coolstore.model.ShoppingCart;
import com.redhat.coolstore.model.ShoppingCartItem;

@Stateful
public class Sh
```

After:

```

import org.eclipse.microprofile.rest.client.inject.RestClient;

import com.redhat.coolstore.model.Product;
import com.redhat.coolstore.model.ShoppingCart;
import com.redhat.coolstore.model.ShoppingCartItem;
import com.redhat.coolstore.rest.client.ShippingServiceClient;

@SessionScoped
public class
```

</details>

### quarkus/springboot / ee-to-quarkus-00020

_40 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Import `jakarta.transaction.Transactional` (not javax)
- When migrating from @MessageDriven EJBs to reactive messaging, add `@Blocking` annotation alongside `@Transactional`
- Replace `@MessageDriven` class-level annotation with `@ApplicationScoped`
- Replace `MessageListener` interface with `@Incoming("channel-name")` method annotation
- Update method signature from `onMessage(Message)` to handle direct message payload types

ORDERING: Apply `@Transactional` during the same refactoring pass that converts EJB annotations to CDI/reactive messaging patterns

<details><summary><code>src/main/java/com/redhat/coolstore/service/CatalogService.java</code></summary>

Before:

```
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@Stateless
public class CatalogService {

    @Injec
```

After:

```

import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;

import jakarta.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@ApplicationScoped
public class CatalogService {

    @Inject
    Logge
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/CatalogService.java</code></summary>

Before:

```

import javax.ejb.Stateless;
import javax.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@Stateless
public class CatalogService {

    @Inject
    Logger log;

    @Inject
    private EntityManager em;

    public CatalogService() {
    }

    public List<CatalogItemEntity> getCat
```

After:

```
import jakarta.persistence.criteria.Root;

import jakarta.persistence.EntityManager;

import com.redhat.coolstore.model.*;

@ApplicationScoped
public class CatalogService {

    @Inject
    Logger log;

    @Inject
    private EntityManager em;

    public CatalogService() {
    }

    public List<C
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/CatalogService.java</code></summary>

Before:

```

import com.redhat.coolstore.model.*;

@Stateless
public class CatalogService {

    @Inject
    Logger log;

    @Inject
    private EntityManager em;

    public CatalogService() {
    }

    public List<CatalogItemEntity> getCatalogItems() {
        CriteriaBuilder cb = em.getCriteriaBuilder();

```

After:

```

import com.redhat.coolstore.model.*;

@ApplicationScoped
public class CatalogService {

    @Inject
    Logger log;

    @Inject
    private EntityManager em;

    public CatalogService() {
    }

    public List<CatalogItemEntity> getCatalogItems() {
        CriteriaBuilder cb = em.getCriteriaBuil
```

</details>

### quarkus/springboot / jakarta-cdi-to-quarkus-00040

_8 incidents, 0 skipped_

GOTCHAS: If the producer method is the only way to provide EntityManager injection in the application, removing the entire Resources class (as in Example 1) means you need an alternative injection mechanism - Quarkus provides EntityManager injection automatically.

ACCOMPANYING CHANGES:

- Update imports from javax._ to jakarta._ packages when touching files with @Produces violations
- May need to remove entire producer classes if they only existed to provide basic CDI producers that Quarkus handles automatically
- Ensure quarkus-hibernate-orm extension is added to dependencies if removing EntityManager producer classes

ORDERING: Remove @Produces annotations after confirming Quarkus extensions (quarkus-arc, quarkus-hibernate-orm) are configured, as these provide the automatic injection capabilities.

<details><summary><code>src/main/java/com/redhat/coolstore/persistence/Resources.java</code></summary>

Before:

```
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Dependent
public class Resources {

    @PersistenceContext
    private EntityManager em;

    @Produces
    public EntityManager getEntityManager() {
        return em;
    }
}

```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/rest/CartEndpoint.java</code></summary>

Before:

```
public class CartEndpoint implements Serializable {

	private static final long serialVersionUID = -7227732980791688773L;

	@Inject
	private ShoppingCartService shoppingCartService;

	@GET
	@Path("/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart getCart(@PathParam("cartId") St
```

After:

```
public class CartEndpoint implements Serializable {

	private static final long serialVersionUID = -7227732980791688773L;

	@Inject
	private ShoppingCartService shoppingCartService;

	@GET
	@Path("/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart getCart(@PathParam("cartId") St
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/rest/CartEndpoint.java</code></summary>

Before:

```
	@GET
	@Path("/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
		return shoppingCartService.getShoppingCart(cartId);
	}

	@POST
	@Path("/checkout/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart checkout(@Path
```

After:

```
	@GET
	@Path("/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
		return shoppingCartService.getShoppingCart(cartId);
	}

	@POST
	@Path("/checkout/{cartId}")
	@Produces(MediaType.APPLICATION_JSON)
	public ShoppingCart checkout(@Path
```

</details>

### quarkus/springboot / javaee-pom-to-quarkus-00030

_1 incidents, 0 skipped_

GOTCHAS:

- Update Java version to 21 (not 11 as shown in example) for Quarkus 3.12.3
- Don't add compiler plugin if parent POM already defines it - check inheritance first

ACCOMPANYING CHANGES:

- Update maven.compiler.release to 21 instead of 11
- May need to update compiler-plugin.version to 3.11.0+ for Java 21 support
- Remove any existing maven-compiler-plugin configuration that conflicts

ORDERING: Must happen before any Java 21 specific code changes or Quarkus extension additions

### quarkus/springboot / javaee-pom-to-quarkus-00040

_1 incidents, 0 skipped_

GOTCHAS: The version 3.0.0 shown in the example may not be compatible with Java 21 - use 3.0.0-M9 or later for Java 21 support.

ACCOMPANYING CHANGES:

- Ensure the `maven.home` system property is actually available in your build environment, or remove it if not needed
- If migrating from an older Surefire version, remove any conflicting `<argLine>` configurations that might interfere with the JBoss LogManager
- May need to add `<useModulePath>false</useModulePath>` if using Java modules and encountering classpath issues

ORDERING: Apply this after updating to Java 21 in the maven-compiler-plugin configuration to ensure version compatibility.

### quarkus/springboot / javaee-pom-to-quarkus-00050

_1 incidents, 0 skipped_

GOTCHAS:

- The incident message shows a typo with nested <goals> tags - should be <goal>integration-test</goal> and <goal>verify</goal>, not wrapped in additional <goals> elements
- Property name mismatch: the example shows <surefire-plugin.version> in properties but references ${compiler-plugin.version} in the plugin version

ACCOMPANYING CHANGES:

- May need to add quarkus-junit5 dependency if not already present for integration tests
- Integration test classes should follow \*IT.java naming convention to be picked up by Failsafe
- Consider adding maven-surefire-plugin configuration for unit tests if not already configured

ORDERING: Add Failsafe plugin after core Quarkus plugins (quarkus-maven-plugin) are already configured

### quarkus/springboot / javaee-pom-to-quarkus-00060

_1 incidents, 0 skipped_

GOTCHAS:

- The native profile may conflict with existing profiles that have overlapping properties or activation criteria
- If skipITs property is already defined elsewhere in the POM, the native profile value may not override correctly due to Maven property precedence

ACCOMPANYING CHANGES:

- Ensure quarkus-maven-plugin is present in the build plugins section with version matching Quarkus BOM
- May need to add native-specific system properties or JVM arguments in the profile for applications with reflection-heavy code
- Consider adding memory/time limits for native builds: <quarkus.native.native-image-xmx>4g</quarkus.native.native-image-xmx>

ORDERING: Add this profile after migrating to Quarkus dependencies and BOM, but before attempting any native compilation testing

### quarkus/springboot / jaxrs-to-quarkus-00020

_2 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Update imports from javax.ws.rs._ to jakarta.ws.rs._ namespace
- Consider removing the entire Application class and @ApplicationPath annotation if you want Quarkus to auto-discover JAX-RS resources at the default root path

GOTCHAS: If you keep the @ApplicationPath annotation, it will still work in Quarkus but defines the base path for all JAX-RS resources. Removing it entirely lets Quarkus use its default behavior and configuration-based path setup via quarkus.resteasy.path property.

<details><summary><code>src/main/java/com/redhat/coolstore/rest/RestApplication.java</code></summary>

Before:

```
package com.redhat.coolstore.rest;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;


@ApplicationPath("/services")
public class RestApplication extends Application {

}

```

After:

```
package com.redhat.coolstore.rest;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;


@ApplicationPath("/services")
public class RestApplication extends Application {

}

```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/rest/RestApplication.java</code></summary>

Before:

```
package com.redhat.coolstore.rest;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;


@ApplicationPath("/services")
public class RestApplication extends Application {

}

```

After:

```
package com.redhat.coolstore.rest;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;


@ApplicationPath("/services")
public class RestApplication extends Application {

}

```

</details>

### quarkus/springboot / jms-to-reactive-quarkus-00010

_1 incidents, 0 skipped_

GOTCHAS:

- Simply replacing @MessageDriven with @ApplicationScoped breaks message processing - need reactive messaging
- JMS configuration in activation properties must be moved to application.properties

ACCOMPANYING CHANGES:

- Replace MessageListener interface implementation with @Incoming annotation on method
- Add @Blocking annotation if processing is synchronous/blocking
- Add @Transactional for database operations previously handled by EJB container
- Change method signature from onMessage(Message) to method accepting String directly
- Remove JMS exception handling - reactive messaging handles message extraction
- Add quarkus-smallrye-reactive-messaging dependency
- Configure message channels in application.properties (mp.messaging.incoming.channelname.\*)

ORDERING: Add reactive messaging dependency before changing annotations

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
import javax.inject.Inject;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

@MessageDriven(name = "OrderServiceMDB", activationConfig =
```

After:

```
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;

@ApplicationScoped
public class OrderServiceMDB {

	@Inje
```

</details>

### quarkus/springboot / jms-to-reactive-quarkus-00020

_3 incidents, 0 skipped_

GOTCHAS:

- The channel name in @Incoming annotation must match configuration - extract from destinationLookup property value (e.g., "topic/orders" becomes "orders")
- Message parameter type changes from javax.jms.Message to direct payload type (String, byte[], etc.)

ACCOMPANYING CHANGES:

- Replace @MessageDriven annotation with @ApplicationScoped
- Remove MessageListener interface implementation
- Remove @Override from onMessage method
- Add @Blocking annotation for synchronous processing
- Add @Transactional if database operations are performed
- Update imports: replace javax.ejb/javax.jms with jakarta.enterprise.context and org.eclipse.microprofile.reactive.messaging
- Remove JMS-specific exception handling and message casting logic
- Simplify method body to work directly with payload instead of extracting from JMS Message

ORDERING: Must add quarkus-smallrye-reactive-messaging dependency to pom.xml before compilation

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

@MessageDriven(name = "OrderServiceMDB", activationConfig = {
	@ActivationConfigProperty
```

After:

```

import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;

@ApplicationScoped
public class OrderServiceMDB {

	@Inject
	OrderService orderService;

	@Inject

```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

@MessageDriven(name = "OrderServiceMDB", activationConfig = {
	@ActivationConfigProperty(propertyName = "destinationLoo
```

After:

```
import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;

@ApplicationScoped
public class OrderServiceMDB {

	@Inject
	OrderService orderService;

	@Inject
	C
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

@MessageDriven(name = "OrderServiceMDB", activationConfig = {
	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "top
```

After:

```

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;

@ApplicationScoped
public class OrderServiceMDB {

	@Inject
	OrderService orderService;

	@Inject
	CatalogService catalogService;

	@Incoming("orders")
	@Blockin
```

</details>

### quarkus/springboot / jms-to-reactive-quarkus-00040

_1 incidents, 0 skipped_

GOTCHAS:

- The @Broadcast annotation is needed when multiple consumers should receive the same message (mimicking JMS Topic behavior)
- Message sending changes from context.createProducer().send() to direct emitter.send() call

ACCOMPANYING CHANGES:

- Replace @Stateless with @RequestScoped (or appropriate scope)
- Remove JMSContext injection and Topic resource injection
- Add MicroProfile Reactive Messaging imports (Channel, Emitter)
- Add SmallRye-specific @Broadcast import if multiple consumers needed
- Update method calls from JMS producer pattern to direct emitter.send()

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java</code></summary>

Before:

```

    @Inject
    Logger log;


    @Inject
    private transient JMSContext context;

    @Resource(lookup = "java:/topic/orders")
    private Topic ordersTopic;



    public void  process(ShoppingCart cart) {
        log.info("Sending order from processor: ");
        context.createProducer(
```

After:

```
@RequestScoped
public class ShoppingCartOrderProcessor  {

    @Inject
    Logger log;

    @Inject
    @Broadcast
    @Channel("orders")
    Emitter<String> ordersEmitter;

    public void  process(ShoppingCart cart) {
        log.info("Sending order from processor: ");
        ordersEmitter.send
```

</details>

### quarkus/springboot / jms-to-reactive-quarkus-00050

_7 incidents, 0 skipped_

GOTCHAS:

- Message-driven beans become regular classes - remove implements MessageListener and @Override annotations
- Channel names in @Incoming must match messaging configuration (e.g., "orders" channel)
- Message payload extraction changes from JMS Message handling to direct parameter types

ACCOMPANYING CHANGES:

- Replace @MessageDriven with @ApplicationScoped
- Add @Incoming annotation with channel name from destinationLookup value
- Add @Blocking and @Transactional annotations for synchronous processing
- Change method signature from onMessage(Message) to onMessage(String) or appropriate payload type
- Remove JMS exception handling and message type checking
- Remove JMS connection/session management code (init(), close() methods)
- Add imports: org.eclipse.microprofile.reactive.messaging.Incoming, io.smallrye.common.annotation.Blocking
- Update from javax._ to jakarta._ package imports

ORDERING: Ensure reactive messaging extensions are added to pom.xml before converting MDBs

<details><summary><code>src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import javax.inject.Inject;
import javax.jms.*;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.rmi.Port
```

After:

```
package com.redhat.coolstore.service;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.utils.Transformers;

import io.smallrye.common.annotation.Blocking;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import javax.ejb.ActivationConfigProperty;
import javax.ejb.MessageDriven;
import javax.inject.Inject;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Or
```

After:

```
package com.redhat.coolstore.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.util
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java</code></summary>

Before:

```
package com.redhat.coolstore.service;

import javax.ejb.ActivationConfigProperty;
import javax.ejb.MessageDriven;
import javax.inject.Inject;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import com.redhat.coolstore.model.Or
```

After:

```
package com.redhat.coolstore.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import org.eclipse.microprofile.reactive.messaging.Incoming;

import com.redhat.coolstore.model.Order;
import com.redhat.coolstore.util
```

</details>

### quarkus/springboot / jndi-to-quarkus-00001

_2 incidents, 0 skipped_

GOTCHAS:

- Don't just replace JNDI lookups line-by-line; often the entire lookup method can be deleted
- JNDI-based remote EJB calls need to be replaced with REST clients or local CDI beans, not just injected

ACCOMPANYING CHANGES:

- Remove unused JNDI-related imports (Context, InitialContext, NamingException, Hashtable)
- Replace @Stateful EJBs with @SessionScoped CDI beans
- Replace remote service calls with @RestClient injected REST clients
- Convert JMS MessageListener to @Incoming reactive messaging methods
- Add MicroProfile annotations (@Blocking, @Transactional) for messaging methods
- Remove manual connection management code (init/close methods) when moving to reactive messaging

ORDERING: Must happen after adding appropriate Quarkus extensions (quarkus-rest-client, quarkus-messaging) to pom.xml

<details><summary><code>src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java</code></summary>

Before:

```
        tsession.close();
        tcon.close();
    }

    private static InitialContext getInitialContext() throws NamingException {
        Hashtable<String, String> env = new Hashtable<>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, JNDI_FACTORY);
        env.put(Context.PROVIDER_URL, "t3:/
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartService.java</code></summary>

Before:

```
    public Product getProduct(String itemId) {
        return productServices.getProductByItemId(itemId);
    }

	private static ShippingServiceRemote lookupShippingServiceRemote() {
        try {
            final Hashtable<String, String> jndiProperties = new Hashtable<>();
            jndiPropert
```

After:

```

    public Product getProduct(String itemId) {
        return productServices.getProductByItemId(itemId);
    }
}

```

</details>

### quarkus/springboot / jndi-to-quarkus-00002

_3 incidents, 0 skipped_

GOTCHAS:

- When removing JNDI lookup methods, check all call sites - they may need complete architectural changes (EJB remote calls → REST clients, JMS manual setup → reactive messaging)
- Don't just replace the lookup() call - often the entire surrounding infrastructure code becomes obsolete

ACCOMPANYING CHANGES:

- Remove entire JNDI-related infrastructure methods and fields, not just the lookup() calls
- Update imports: remove javax.naming._, javax.jms._ and add appropriate Quarkus/MicroProfile imports
- Change class annotations: @Stateful → @SessionScoped, add @RestClient for injected services
- For JMS: replace MessageListener interface with @Incoming reactive messaging methods
- Add @Blocking and @Transactional annotations for message handlers that do blocking operations
- Update method signatures: JMS Message parameter → direct String/object parameter
- Remove manual connection management code (init(), close() methods)

<details><summary><code>src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java</code></summary>

Before:

```

            } catch (JMSException jmse) {
                System.err.println("An exception occurred: " + jmse.getMessage());
            }
        }
    }

    public void init() throws NamingException, JMSException {
        Context ctx = getInitialContext();
        TopicConnectionFactory tconFac
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java</code></summary>

Before:

```
            }
        }
    }

    public void init() throws NamingException, JMSException {
        Context ctx = getInitialContext();
        TopicConnectionFactory tconFactory = (TopicConnectionFactory) PortableRemoteObject.narrow(ctx.lookup(JMS_FACTORY), TopicConnectionFactory.class);
        tc
```

</details>

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShoppingCartService.java</code></summary>

Before:

```
    }

	private static ShippingServiceRemote lookupShippingServiceRemote() {
        try {
            final Hashtable<String, String> jndiProperties = new Hashtable<>();
            jndiProperties.put(Context.INITIAL_CONTEXT_FACTORY, "org.wildfly.naming.client.WildFlyInitialContextFactory");


```

After:

```
        return productServices.getProductByItemId(itemId);
    }
}

```

</details>

### quarkus/springboot / persistence-to-quarkus-00000

_1 incidents, 0 skipped_

GOTCHAS:

- The persistence.xml file should be completely removed after migration, not just emptied
- Property name mappings are not always 1:1 (e.g., hibernate.hbm2ddl.auto becomes quarkus.hibernate-orm.database.generation with different values)

ACCOMPANYING CHANGES:

- Remove datasource XML files (e.g., \*-ds.xml files in WEB-INF or test resources)
- Remove META-INF/persistence.xml entirely after extracting configuration
- Add quarkus-hibernate-orm and quarkus-jdbc-\* extensions to pom.xml if not already present
- Update any @PersistenceContext or @PersistenceUnit annotations to use default persistence unit (remove unitName attributes)

ORDERING: Must happen after Quarkus extensions are added to pom.xml but before removing Java EE dependencies

### quarkus/springboot / persistence-to-quarkus-00010

_1 incidents, 0 skipped_

ACCOMPANYING CHANGES:

- Remove `@Produces` methods that were used to expose EntityManager - Quarkus CDI handles injection directly
- Delete entire producer classes/methods if they only exist to produce EntityManager instances
- Update imports: remove `javax.persistence.PersistenceContext` and `javax.enterprise.inject.Produces`, add `javax.inject.Inject`
- Remove `@Dependent` scope annotations from producer classes that are being deleted

GOTCHAS:

- Don't just replace the annotation - if the EntityManager was produced via a `@Produces` method, remove the entire producer pattern as it's redundant in Quarkus

<details><summary><code>src/main/java/com/redhat/coolstore/persistence/Resources.java</code></summary>

Before:

```

import javax.enterprise.context.Dependent;
import javax.enterprise.inject.Produces;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Dependent
public class Resources {

    @PersistenceContext
    private EntityManager em;

    @Produces
    public EntityManage
```

</details>

### quarkus/springboot / persistence-to-quarkus-00011

_1 incidents, 0 skipped_

GOTCHAS: If the EntityManager producer is completely removed, ensure all injection points in the codebase are updated to use simple @Inject instead of any custom qualifiers that may have been used with the producer.

ACCOMPANYING CHANGES:

- Remove the entire producer class file if it only contained the EntityManager producer and has no other functionality
- Update all @Inject points that were using the produced EntityManager to use direct injection
- Remove unused imports (javax.enterprise.inject.Produces, javax.persistence.PersistenceContext, javax.enterprise.context.Dependent)
- Ensure datasource configuration is properly set in application.properties for automatic EntityManager creation

<details><summary><code>src/main/java/com/redhat/coolstore/persistence/Resources.java</code></summary>

Before:

```
import javax.persistence.PersistenceContext;

@Dependent
public class Resources {

    @PersistenceContext
    private EntityManager em;

    @Produces
    public EntityManager getEntityManager() {
        return em;
    }
}

```

</details>

### quarkus/springboot / remote-ejb-to-quarkus-00000

_1 incidents, 0 skipped_

GOTCHAS:

- Remove the remote interface implementation (e.g., `implements ShippingServiceRemote`) from the class declaration
- Don't forget to remove @Override annotations from methods that were implementing the remote interface

ACCOMPANYING CHANGES:

- Remove imports for javax.ejb.Remote and javax.ejb.Stateless
- Add imports for jakarta.ws.rs.POST, jakarta.ws.rs.Path, and jakarta.ws.rs.GET as needed
- Delete the corresponding remote interface file (e.g., ShippingServiceRemote.java) as it's no longer needed
- Update any client code that was injecting the remote EJB to use REST client calls instead

ORDERING: Convert remote EJBs before updating client code that depends on them

<details><summary><code>src/main/java/com/redhat/coolstore/service/ShippingService.java</code></summary>

Before:

```
import java.math.BigDecimal;
import java.math.RoundingMode;

import javax.ejb.Remote;
import javax.ejb.Stateless;

import com.redhat.coolstore.model.ShoppingCart;

@Stateless
@Remote
public class ShippingService implements ShippingServiceRemote {

    @Override
    public double calculateShipping(Sh
```

After:

```
import java.math.BigDecimal;
import java.math.RoundingMode;

import com.redhat.coolstore.model.ShoppingCart;

import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;

@Path("/shipping")
public class ShippingService {

    @POST
    @Path("/calculateShipping")
    public double calculateShipping(Shoppi
```

</details>
