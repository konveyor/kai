# quarkus/springboot
## Description
This ruleset gives hints to migrate from SpringBoot devtools to Quarkus
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 20
### #0 - cdi-to-quarkus-00030
* Category: potential
* Effort: 3
* Description: `beans.xml` descriptor content is ignored
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Incidents
  * file:///opt/input/source/src/main/webapp/WEB-INF/beans.xml
      * Line Number: 18
      * Message: '`beans.xml` descriptor content is ignored and it could be removed from the application. 
 Refer to the guide referenced below to check the supported CDI feature in Quarkus.'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <!--
  3      JBoss, Home of Professional Open Source
  4      Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
  5      contributors by the @authors tag. See the copyright.txt in the
  6      distribution for a full listing of individual contributors.
  7      Licensed under the Apache License, Version 2.0 (the "License");
  8      you may not use this file except in compliance with the License.
  9      You may obtain a copy of the License at
 10      http://www.apache.org/licenses/LICENSE-2.0
 11      Unless required by applicable law or agreed to in writing, software
 12      distributed under the License is distributed on an "AS IS" BASIS,
 13      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 14      See the License for the specific language governing permissions and
 15      limitations under the License.
 16  -->
 17  <!-- Marker file indicating CDI should be enabled -->
 18  <beans xmlns="http://xmlns.jcp.org/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 19  	   xsi:schemaLocation="
 20        http://xmlns.jcp.org/xml/ns/javaee
 21        http://xmlns.jcp.org/xml/ns/javaee/beans_1_1.xsd"
 22  	   bean-discovery-mode="all">
 23  </beans>

```
### #1 - cdi-to-quarkus-00040
* Category: potential
* Effort: 1
* Description: Producer annotation no longer required
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus Simplified Producer Method Declaration: https://quarkus.io/guides/cdi-reference#simplified-producer-method-declaration
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 14
      * Message: 'In Quarkus, you can skip the @Produces annotation completely if the producer method is annotated with a scope annotation, a stereotype or a qualifier..
 This field could be accessed using a `@Named` getter method instead.'
      * Code Snippet:
```java
 4  import javax.enterprise.inject.Produces;
 5  import javax.persistence.EntityManager;
 6  import javax.persistence.PersistenceContext;
 7  
 8  @Dependent
 9  public class Resources {
10  
11      @PersistenceContext
12      private EntityManager em;
13  
14      @Produces
15      public EntityManager getEntityManager() {
16          return em;
17      }
18  }

```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Producers.java
      * Line Number: 12
      * Message: 'In Quarkus, you can skip the @Produces annotation completely if the producer method is annotated with a scope annotation, a stereotype or a qualifier..
 This field could be accessed using a `@Named` getter method instead.'
      * Code Snippet:
```java
 2  
 3  import javax.enterprise.inject.Produces;
 4  import javax.enterprise.inject.spi.InjectionPoint;
 5  import java.util.logging.Logger;
 6  
 7  
 8  public class Producers {
 9  
10      Logger log = Logger.getLogger(Producers.class.getName());
11  
12      @Produces
13      public Logger produceLog(InjectionPoint injectionPoint) {
14          return Logger.getLogger(injectionPoint.getMember().getDeclaringClass().getName());
15      }
16  
17  }

```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/enterprise/inject/Produces.java
      * Line Number: 120
      * Message: 'In Quarkus, you can skip the @Produces annotation completely if the producer method is annotated with a scope annotation, a stereotype or a qualifier..
 This field could be accessed using a `@Named` getter method instead.'
      * Code Snippet:
```java
110   * 
111   * @see javax.enterprise.inject.Disposes &#064;Disposes
112   * 
113   * @author Gavin King
114   * @author Pete Muir
115   */
116  
117  @Target({ METHOD, FIELD })
118  @Retention(RUNTIME)
119  @Documented
120  public @interface Produces {
121  }

```
### #2 - ee-to-quarkus-00000
* Category: potential
* Effort: 1
* Description: @Stateless annotation must be replaced
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus CDI reference: https://quarkus.io/guides/cdi-reference
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 17
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
 7  
 8  import javax.persistence.criteria.CriteriaBuilder;
 9  import javax.persistence.criteria.CriteriaQuery;
10  import javax.persistence.criteria.Root;
11  
12  import javax.ejb.Stateless;
13  import javax.persistence.EntityManager;
14  
15  import com.redhat.coolstore.model.*;
16  
17  @Stateless
18  public class CatalogService {
19  
20      @Inject
21      Logger log;
22  
23      @Inject
24      private EntityManager em;
25  
26      public CatalogService() {
27      }
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 12
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
 2  
 3  import com.redhat.coolstore.model.Order;
 4  import java.util.List;
 5  import javax.ejb.Stateless;
 6  import javax.inject.Inject;
 7  import javax.persistence.EntityManager;
 8  import javax.persistence.criteria.CriteriaBuilder;
 9  import javax.persistence.criteria.CriteriaQuery;
10  import javax.persistence.criteria.Root;
11  
12  @Stateless
13  public class OrderService {
14  
15    @Inject
16    private EntityManager em;
17  
18    public void save(Order order) {
19      em.persist(order);
20    }
21  
22    public List<Order> getOrders() {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ProductService.java
      * Line Number: 14
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
 4  import com.redhat.coolstore.model.Product;
 5  import com.redhat.coolstore.utils.Transformers;
 6  
 7  import javax.ejb.Stateless;
 8  import javax.inject.Inject;
 9  import java.util.List;
10  import java.util.stream.Collectors;
11  
12  import static com.redhat.coolstore.utils.Transformers.toProduct;
13  
14  @Stateless
15  public class ProductService {
16  
17      @Inject
18      CatalogService cm;
19  
20      public ProductService() {
21      }
22  
23      public List<Product> getProducts() {
24          return cm.getCatalogItems().stream().map(entity -> toProduct(entity)).collect(Collectors.toList());
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 11
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.math.BigDecimal;
 4  import java.math.RoundingMode;
 5  
 6  import javax.ejb.Remote;
 7  import javax.ejb.Stateless;
 8  
 9  import com.redhat.coolstore.model.ShoppingCart;
10  
11  @Stateless
12  @Remote
13  public class ShippingService implements ShippingServiceRemote {
14  
15      @Override
16      public double calculateShipping(ShoppingCart sc) {
17  
18          if (sc != null) {
19  
20              if (sc.getCartItemTotal() >= 0 && sc.getCartItemTotal() < 25) {
21  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 13
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
 3  import java.util.logging.Logger;
 4  import javax.ejb.Stateless;
 5  import javax.annotation.Resource;
 6  import javax.inject.Inject;
 7  import javax.jms.JMSContext;
 8  import javax.jms.Topic;
 9  
10  import com.redhat.coolstore.model.ShoppingCart;
11  import com.redhat.coolstore.utils.Transformers;
12  
13  @Stateless
14  public class ShoppingCartOrderProcessor  {
15  
16      @Inject
17      Logger log;
18  
19  
20      @Inject
21      private transient JMSContext context;
22  
23      @Resource(lookup = "java:/topic/orders")
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ejb/Stateless.java
      * Line Number: 62
      * Message: 'Stateless EJBs can be converted to a CDI bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
52  import static java.lang.annotation.RetentionPolicy.*;
53  
54  /**
55   * Component-defining annotation for a stateless session bean.
56   *
57   * @since EJB 3.0
58   */
59  
60  @Target(TYPE) 
61  @Retention(RUNTIME)
62  public @interface Stateless {
63  
64      /**
65       * The ejb-name for this bean.  Defaults to the unqualified name of the
66       * stateless session bean class.
67       */
68      String name() default "";
69  
70      /**
71        * A product specific name(e.g. global JNDI name) 
72        * that this session bean should be mapped to.  
```
### #3 - ee-to-quarkus-00010
* Category: mandatory
* Effort: 3
* Description: @Stateful annotation must be replaced
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus CDI reference: https://quarkus.io/guides/cdi-reference
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartService.java
      * Line Number: 16
      * Message: 'Stateful EJBs can be converted to a CDI bean by replacing the `@Stateful` annotation with a bean-defining annotation
 that encompasses the appropriate scope (e.g., `@ApplicationScoped`). `@Stateful` EJBs often translate to `@SessionScoped`
 beans (a scope which requires activating the `quarkus-undertow` extension), but the appropriate scope may differ based
 on your application architecture. Review your application's requirements to determine the appropriate scope.

 Note that it is recommended, as a good practice, to keep state external from the service in Quarkus.'
      * Code Snippet:
```java
 6  import javax.ejb.Stateful;
 7  import javax.inject.Inject;
 8  import javax.naming.Context;
 9  import javax.naming.InitialContext;
10  import javax.naming.NamingException;
11  
12  import com.redhat.coolstore.model.Product;
13  import com.redhat.coolstore.model.ShoppingCart;
14  import com.redhat.coolstore.model.ShoppingCartItem;
15  
16  @Stateful
17  public class ShoppingCartService  {
18  
19      @Inject
20      Logger log;
21  
22      @Inject
23      ProductService productServices;
24  
25      @Inject
26      PromoService ps;
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ejb/Stateful.java
      * Line Number: 56
      * Message: 'Stateful EJBs can be converted to a CDI bean by replacing the `@Stateful` annotation with a bean-defining annotation
 that encompasses the appropriate scope (e.g., `@ApplicationScoped`). `@Stateful` EJBs often translate to `@SessionScoped`
 beans (a scope which requires activating the `quarkus-undertow` extension), but the appropriate scope may differ based
 on your application architecture. Review your application's requirements to determine the appropriate scope.

 Note that it is recommended, as a good practice, to keep state external from the service in Quarkus.'
      * Code Snippet:
```java
46  import static java.lang.annotation.RetentionPolicy.*;
47  
48  /**
49   * Component-defining annotation for a stateful session bean.
50   *
51   * @since EJB 3.0
52   */
53  
54  @Target(TYPE) 
55  @Retention(RUNTIME)
56  public @interface Stateful {
57  
58      /**
59       * The ejb-name for this bean.  Defaults to the unqualified name of
60       * the stateful session bean class.
61       */
62      String name() default "";
63  
64      /**
65        * A product specific name(e.g. global JNDI name) 
66        * that this session bean should be mapped to.  
```
### #4 - javaee-pom-to-quarkus-00000
* Category: mandatory
* Effort: 1
* Description: The expected project artifact's extension is `jar`
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 9
      * Message: 'The project artifact's current extension (i.e. `<packaging>` tag value) is `` but the expected value should be `jar`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #5 - javaee-pom-to-quarkus-00010
* Category: mandatory
* Effort: 1
* Description: Adopt Quarkus BOM
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
  * Quarkus - Releases: https://quarkus.io/blog/tag/release/
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Use the Quarkus BOM to omit the version of the different Quarkus dependencies. 
 Add the following sections to the `pom.xml` file: 

 ```xml
 <properties> 
 <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id> 
 <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id> 
 <quarkus.platform.version>3.1.0.Final</quarkus.platform.version>
 </properties> 
 <dependencyManagement> 
 <dependencies> 
 <dependency> 
 <groupId>$</groupId> 
 <artifactId>$</artifactId> 
 <version>$</version> 
 <type>pom</type> 
 <scope>import</scope> 
 </dependency> 
 </dependencies> 
 </dependencyManagement> 
 ```
 Check the latest Quarkus version available from the `Quarkus - Releases` link below.'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #6 - javaee-pom-to-quarkus-00020
* Category: mandatory
* Effort: 1
* Description: Adopt Quarkus Maven plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Use the Quarkus Maven plugin adding the following sections to the `pom.xml` file: 

 ```xml
 <properties> 
 <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id> 
 <quarkus.platform.version>3.1.0.Final</quarkus.platform.version>
 </properties> 
 <build>
 <plugins>
 <plugin>
 <groupId>$</groupId>
 <artifactId>quarkus-maven-plugin</artifactId>
 <version>$</version>
 <extensions>true</extensions>
 <executions>
 <execution>
 <goals>
 <goal>build</goal>
 <goal>generate-code</goal>
 <goal>generate-code-tests</goal>
 </goals>
 </execution>
 </executions>
 </plugin>
 </plugins>
 </build>
 ```'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #7 - javaee-pom-to-quarkus-00030
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Compiler plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Use the Maven Compiler plugin adding the following sections to the `pom.xml` file: 

 ```xml
 <properties> 
 <compiler-plugin.version>3.10.1</compiler-plugin.version>
 <maven.compiler.release>11</maven.compiler.release>
 </properties> 
 <build>
 <plugins>
 <plugin>
 <artifactId>maven-compiler-plugin</artifactId>
 <version>$</version>
 <configuration>
 <compilerArgs>
 <arg>-parameters</arg>
 </compilerArgs>
 </configuration>
 </plugin>
 </plugins>
 </build>
 ```'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #8 - javaee-pom-to-quarkus-00040
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Surefire plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Use the Maven Surefire plugin adding the following sections to the `pom.xml` file: 

 ```xml
 <properties> 
 <surefire-plugin.version>3.0.0</compiler-plugin.version>
 </properties> 
 <build>
 <plugins>
 <plugin>
 <artifactId>maven-surefire-plugin</artifactId>
 <version>$</version>
 <configuration>
 <systemPropertyVariables>
 <java.util.logging.manager>org.jboss.logmanager.LogManager</java.util.logging.manager>
 <maven.home>$</maven.home>
 </systemPropertyVariables>
 </configuration>
 </plugin>
 </plugins>
 </build>
 ```'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #9 - javaee-pom-to-quarkus-00050
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Failsafe plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Use the Maven Failsafe plugin adding the following sections to the `pom.xml` file: 

 ```xml
 <properties> 
 <surefire-plugin.version>3.0.0</compiler-plugin.version>
 </properties> 
 <build>
 <plugins>
 <plugin>
 <artifactId>maven-failsafe-plugin</artifactId>
 <version>$</version>
 <executions>
 <execution>
 <goals>
 <goals>integration-test</goal>
 <goals>verify</goal>
 </goals>
 <configuration>
 <systemPropertyVariables>
 <native.image.path>$/$-runner</native.image.path>
 <java.util.logging.manager>org.jboss.logmanager.LogManager</java.util.logging.manager>
 <maven.home>$</maven.home>
 </systemPropertyVariables>
 </configuration>
 </execution>
 </executions>
 </plugin>
 </plugins>
 </build>
 ```'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #10 - javaee-pom-to-quarkus-00060
* Category: mandatory
* Effort: 1
* Description: Add Maven profile to run the Quarkus native build
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide;: https://quarkus.io/guides/maven-tooling#build-tool-maven;
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 5
      * Message: 'Leverage a Maven profile to run the Quarkus native build adding the following section to the `pom.xml` file: 

 ```xml
 <profiles>
 <profile>
 <id>native</id>
 <activation>
 <property>
 <name>native</name>
 </property>
 </activation>
 <properties>
 <skipITs>false</skipITs>
 <quarkus.package.type>native</quarkus.package.type>
 </properties>
 </profile>
 </profiles>
 ```'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <project 
  3      xmlns="http://maven.apache.org/POM/4.0.0" 
  4      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  5      <modelVersion>4.0.0</modelVersion>
  6      <groupId>com.redhat.coolstore</groupId>
  7      <artifactId>monolith</artifactId>
  8      <version>1.0.0-SNAPSHOT</version>
  9      <packaging>war</packaging>
 10      <name>coolstore-monolith</name>
 11      <properties>
 12          <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
 13          <maven.build.timestamp.format>yyyyMMdd'T'HHmmss</maven.build.timestamp.format>
 14          <project.encoding>UTF-8</project.encoding>
 15          <maven.test.skip>true</maven.test.skip>
 16      </properties>
 17      <dependencies>
 18          <dependency>
 19              <groupId>javax</groupId>
 20              <artifactId>javaee-web-api</artifactId>
 21              <version>7.0</version>
 22              <scope>provided</scope>
 23          </dependency>
 24          <dependency>
 25              <groupId>javax</groupId>
 26              <artifactId>javaee-api</artifactId>
 27              <version>7.0</version>
 28              <scope>provided</scope>
 29          </dependency>
 30          <dependency>
 31              <groupId>org.jboss.spec.javax.jms</groupId>
 32              <artifactId>jboss-jms-api_2.0_spec</artifactId>
 33              <version>2.0.0.Final</version>
 34          </dependency>
 35          <dependency>
 36              <groupId>org.flywaydb</groupId>
 37              <artifactId>flyway-core</artifactId>
 38              <version>4.1.2</version>
 39          </dependency>
 40          <dependency>
 41              <groupId>org.jboss.spec.javax.rmi</groupId>
 42              <artifactId>jboss-rmi-api_1.0_spec</artifactId>
 43              <version>1.0.2.Final</version>
 44          </dependency>
 45      </dependencies>
 46      <build>
 47          <finalName>ROOT</finalName>
 48          <plugins>
 49              <plugin>
 50                  <artifactId>maven-compiler-plugin</artifactId>
 51                  <version>3.0</version>
 52                  <configuration>
 53                      <encoding>${project.encoding}</encoding>
 54                      <source>1.8</source>
 55                      <target>1.8</target>
 56                  </configuration>
 57              </plugin>
 58              <plugin>
 59                  <groupId>org.apache.maven.plugins</groupId>
 60                  <artifactId>maven-war-plugin</artifactId>
 61                  <version>3.2.0</version>
 62              </plugin>
 63          </plugins>
 64      </build>
 65      <profiles>
 66  <!-- TODO: Add OpenShift profile here -->
 67      </profiles>
 68  </project>

```
### #11 - jaxrs-to-quarkus-00020
* Category: optional
* Effort: 1
* Description: JAX-RS activation is no longer necessary
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/resteasy-reactive#declaring-endpoints-uri-mapping
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/RestApplication.java
      * Line Number: 7
      * Message: 'JAX-RS activation is no longer necessary. You can set a root path like this but you don't have to.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import javax.ws.rs.ApplicationPath;
 4  import javax.ws.rs.core.Application;
 5  
 6  
 7  @ApplicationPath("/services")
 8  public class RestApplication extends Application {
 9  
10  }

```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/RestApplication.java
      * Line Number: 8
      * Message: 'JAX-RS activation is no longer necessary. You can set a root path like this but you don't have to.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import javax.ws.rs.ApplicationPath;
 4  import javax.ws.rs.core.Application;
 5  
 6  
 7  @ApplicationPath("/services")
 8  public class RestApplication extends Application {
 9  
10  }

```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ws/rs/ApplicationPath.java
      * Line Number: 65
      * Message: 'JAX-RS activation is no longer necessary. You can set a root path like this but you don't have to.'
      * Code Snippet:
```java
55   *
56   * @author Paul Sandoz
57   * @author Marc Hadley
58   * @see javax.ws.rs.core.Application
59   * @see Path
60   * @since 1.1
61   */
62  @Documented
63  @Target({ElementType.TYPE})
64  @Retention(RetentionPolicy.RUNTIME)
65  public @interface ApplicationPath {
66  
67      /**
68       * Defines the base URI for all resource URIs. A trailing '/' character will
69       * be automatically appended if one is not present.
70       *
71       * <p>The supplied value is automatically percent
72       * encoded to conform to the {@code path} production of
73       * {@link <a href="http://tools.ietf.org/html/rfc3986#section-3.3">RFC 3986 section 3.3</a>}.
74       * Note that percent encoded values are allowed in the value, an
75       * implementation will recognize such values and will not double
```
### #12 - jms-to-reactive-quarkus-00010
* Category: mandatory
* Effort: 3
* Description: @MessageDriven - EJBs are not supported in Quarkus
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 14
      * Message: 'Enterprise Java Beans (EJBs) are not supported in Quarkus. CDI must be used.
 Please replace the `@MessageDriven` annotation with a CDI scope annotation like `@ApplicationScoped`.'
      * Code Snippet:
```java
 4  import javax.ejb.MessageDriven;
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
19  
20  	@Inject
21  	OrderService orderService;
22  
23  	@Inject
24  	CatalogService catalogService;
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ejb/MessageDriven.java
      * Line Number: 62
      * Message: 'Enterprise Java Beans (EJBs) are not supported in Quarkus. CDI must be used.
 Please replace the `@MessageDriven` annotation with a CDI scope annotation like `@ApplicationScoped`.'
      * Code Snippet:
```java
52   * listener interface for the messaging type that the message-driven
53   * bean supports or specify the message listener interface using the
54   * <code>messageListenerInterface</code> element of this annotation.
55   *
56   * @see ActivationConfigProperty
57   *
58   * @since EJB 3.0
59   */
60  @Target({ElementType.TYPE})
61  @Retention(RetentionPolicy.RUNTIME)
62  public @interface MessageDriven {
63  
64      /**
65       * The ejb-name for this bean.  Defaults to the unqualified name of
66       * the message driven bean class.
67       */
68      String name() default "";
69  
70      /**
71       * Message-listener interface.  If the message-driven bean class
72       * implements more than one interface other than <code>java.io.Serializable</code>,
```
### #13 - jms-to-reactive-quarkus-00020
* Category: mandatory
* Effort: 3
* Description: Configure message listener method with @Incoming
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Incoming (SmallRye Reactive Messaging API): https://smallrye.io/smallrye-reactive-messaging/2.5.0/apidocs/org/eclipse/microprofile/reactive/messaging/Incoming.html
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 15
      * Message: 'The `destinationLookup` property can be migrated by annotating a message handler method (potentially `onMessage`) with the
 `org.eclipse.microprofile.reactive.messaging.Incoming` annotation, indicating the name of the queue as a value:
 
 Before:
 ```
 @MessageDriven(name = "HelloWorldQueueMDB", activationConfig = 
 public class MessageListenerImpl implements MessageListener 
 }}
 ```
 
 After:
 ```
 public class MessageListenerImpl implements MessageListener 
 }}
 ```'
      * Code Snippet:
```java
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
19  
20  	@Inject
21  	OrderService orderService;
22  
23  	@Inject
24  	CatalogService catalogService;
25  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 16
      * Message: 'The `destinationLookup` property can be migrated by annotating a message handler method (potentially `onMessage`) with the
 `org.eclipse.microprofile.reactive.messaging.Incoming` annotation, indicating the name of the queue as a value:
 
 Before:
 ```
 @MessageDriven(name = "HelloWorldQueueMDB", activationConfig = 
 public class MessageListenerImpl implements MessageListener 
 }}
 ```
 
 After:
 ```
 public class MessageListenerImpl implements MessageListener 
 }}
 ```'
      * Code Snippet:
```java
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
19  
20  	@Inject
21  	OrderService orderService;
22  
23  	@Inject
24  	CatalogService catalogService;
25  
26  	@Override
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 17
      * Message: 'The `destinationLookup` property can be migrated by annotating a message handler method (potentially `onMessage`) with the
 `org.eclipse.microprofile.reactive.messaging.Incoming` annotation, indicating the name of the queue as a value:
 
 Before:
 ```
 @MessageDriven(name = "HelloWorldQueueMDB", activationConfig = 
 public class MessageListenerImpl implements MessageListener 
 }}
 ```
 
 After:
 ```
 public class MessageListenerImpl implements MessageListener 
 }}
 ```'
      * Code Snippet:
```java
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
19  
20  	@Inject
21  	OrderService orderService;
22  
23  	@Inject
24  	CatalogService catalogService;
25  
26  	@Override
27  	public void onMessage(Message rcvMessage) {
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ejb/ActivationConfigProperty.java
      * Line Number: 99
      * Message: 'The `destinationLookup` property can be migrated by annotating a message handler method (potentially `onMessage`) with the
 `org.eclipse.microprofile.reactive.messaging.Incoming` annotation, indicating the name of the queue as a value:
 
 Before:
 ```
 @MessageDriven(name = "HelloWorldQueueMDB", activationConfig = 
 public class MessageListenerImpl implements MessageListener 
 }}
 ```
 
 After:
 ```
 public class MessageListenerImpl implements MessageListener 
 }}
 ```'
      * Code Snippet:
```java
 89   * the JMS client identifier that will be used when connecting to the JMS provider 
 90   * from which a JMS message-driven bean is to receive messages.
 91   * If this property is not specified then the client identifier will be left unset.
 92   *
 93   * </ul>
 94   *
 95   * @since EJB 3.0
 96   */
 97  @Target({})
 98  @Retention(RetentionPolicy.RUNTIME)
 99  public @interface ActivationConfigProperty {
100      String propertyName();
101      String propertyValue();
102  }

```
### #14 - jms-to-reactive-quarkus-00030
* Category: mandatory
* Effort: 3
* Description: JMS' Queue must be replaced with an Emitter
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Emitter (Microprofile Reactive Streams Messaging): https://smallrye.io/smallrye-reactive-messaging/2.0.2/apidocs/org/eclipse/microprofile/reactive/messaging/Emitter.html
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 994
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
 984  	 * which is done using the {@code createTemporaryQueue} method.
 985  	 * 
 986  	 * @param queueName
 987  	 *            A provider-specific queue name
 988  	 * @return a Queue object which encapsulates the specified name
 989  	 * 
 990  	 * @throws JMSRuntimeException
 991  	 *             if a Queue object cannot be created due to some internal
 992  	 *             error
 993  	 */
 994  	Queue createQueue(String queueName);
 995  
 996  	/**
 997  	 * Creates a {@code Topic} object which encapsulates a specified
 998  	 * provider-specific topic name.
 999  	 * <p>
1000  	 * The use of provider-specific topic names in an application may render the
1001  	 * application non-portable. Portable applications are recommended to not
1002  	 * use this method but instead look up an administratively-defined
1003  	 * {@code Topic} object using JNDI.
1004  	 * <p>
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1504
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
1494  	 *            the {@code queue} to access
1495  	 * 
1496  	 * 
1497  	 * @exception JMSRuntimeException
1498  	 *                if the session fails to create a browser due to some
1499  	 *                internal error.
1500  	 * @exception InvalidRuntimeDestinationException
1501  	 *                if an invalid destination is specified
1502  	 * 
1503  	 */
1504  	QueueBrowser createBrowser(Queue queue);
1505  
1506  	/**
1507  	 * Creates a {@code QueueBrowser} object to peek at the messages on the
1508  	 * specified queue using a message selector.
1509  	 * 
1510  	 * @param queue
1511  	 *            the {@code queue} to access
1512  	 * 
1513  	 * @param messageSelector
1514  	 *            only messages with properties matching the message selector
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1529
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
1519  	 * @exception JMSRuntimeException
1520  	 *                if the session fails to create a browser due to some
1521  	 *                internal error.
1522  	 * @exception InvalidRuntimeDestinationException
1523  	 *                if an invalid destination is specified
1524  	 * @exception InvalidRuntimeSelectorException
1525  	 *                if the message selector is invalid.
1526  	 * 
1527  	 */
1528  
1529  	QueueBrowser createBrowser(Queue queue, String messageSelector);
1530  
1531  	/**
1532  	 * Creates a {@code TemporaryQueue} object. Its lifetime will be that
1533  	 * of the JMSContext's {@code Connection} unless it is deleted earlier.
1534  	 * 
1535  	 * @return a temporary queue identity
1536  	 * 
1537  	 * @exception JMSRuntimeException
1538  	 *                if the session fails to create a temporary queue due to
1539  	 *                some internal error.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/Queue.java
      * Line Number: 69
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
59    * @see Session#createConsumer(Destination)
60    * @see Session#createProducer(Destination)
61    * @see Session#createQueue(String)
62    * @see QueueSession#createQueue(String)
63    * 
64    * @version JMS 2.0
65    * @since JMS 1.0
66    *
67    */
68   
69  public interface Queue extends Destination { 
70  
71      /** Gets the name of this queue.
72        *  
73        * <P>Clients that depend upon the name are not portable.
74        *  
75        * @return the queue name
76        *  
77        * @exception JMSException if the JMS provider implementation of 
78        *                         {@code Queue} fails to return the queue
79        *                         name due to some internal
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueBrowser.java
      * Line Number: 84
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
74  
75      /** Gets the queue associated with this queue browser.
76        * 
77        * @return the queue
78        *  
79        * @exception JMSException if the JMS provider fails to get the
80        *                         queue associated with this browser
81        *                         due to some internal error.
82        */
83  
84      Queue 
85      getQueue() throws JMSException;
86  
87  
88      /** Gets this queue browser's message selector expression.
89        *  
90        * @return this queue browser's message selector, or null if no
91        *         message selector exists for the message consumer (that is, if 
92        *         the message selector was not set or was set to null or the 
93        *         empty string)
94        *
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueConnection.java
      * Line Number: 128
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
118        *                         to create a connection consumer due to some
119        *                         internal error or invalid arguments for 
120        *                         {@code sessionPool} and 
121        *                         {@code messageSelector}.
122        * @exception InvalidDestinationException if an invalid queue is specified.
123        * @exception InvalidSelectorException if the message selector is invalid.
124        * @see javax.jms.ConnectionConsumer
125        */ 
126  
127      ConnectionConsumer
128      createConnectionConsumer(Queue queue,
129                               String messageSelector,
130                               ServerSessionPool sessionPool,
131  			     int maxMessages)
132  			   throws JMSException;
133  }

```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueReceiver.java
      * Line Number: 86
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
76  
77      /** Gets the {@code Queue} associated with this queue receiver.
78        *  
79        * @return this receiver's {@code Queue} 
80        *  
81        * @exception JMSException if the JMS provider fails to get the queue for
82        *                         this queue receiver
83        *                         due to some internal error.
84        */ 
85   
86      Queue
87      getQueue() throws JMSException;
88  }

```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueRequestor.java
      * Line Number: 88
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
78        * @param session the {@code QueueSession} the queue belongs to
79        * @param queue the queue to perform the request/reply call on
80        *  
81        * @exception JMSException if the JMS provider fails to create the
82        *                         {@code QueueRequestor} due to some internal
83        *                         error.
84        * @exception InvalidDestinationException if an invalid queue is specified.
85        */ 
86  
87      public
88      QueueRequestor(QueueSession session, Queue queue) throws JMSException {
89      	
90      	if (queue==null) throw new InvalidDestinationException("queue==null");
91      	
92          this.session = session;
93          tempQueue    = session.createTemporaryQueue();
94          sender       = session.createSender(queue);
95          receiver     = session.createReceiver(tempQueue);
96      }
97  
98  
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSender.java
      * Line Number: 103
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
 93  
 94      /** Gets the queue associated with this {@code QueueSender}.
 95        *  
 96        * @return this sender's queue 
 97        *  
 98        * @exception JMSException if the JMS provider fails to get the queue for
 99        *                         this {@code QueueSender}
100        *                         due to some internal error.
101        */ 
102   
103      Queue
104      getQueue() throws JMSException;
105  
106  
107      /** Sends a message to the queue. Uses the {@code QueueSender}'s 
108        * default delivery mode, priority, and time to live.
109        *
110        * @param message the message to send 
111        *  
112        * @exception JMSException if the JMS provider fails to send the message 
113        *                         due to some internal error.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSender.java
      * Line Number: 181
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
171        * @exception MessageFormatException if an invalid message is specified.
172        * @exception InvalidDestinationException if a client uses
173        *                         this method with an invalid queue.
174        * 
175        * @see javax.jms.MessageProducer#getDeliveryMode()
176        * @see javax.jms.MessageProducer#getTimeToLive()
177        * @see javax.jms.MessageProducer#getPriority()
178        */ 
179   
180      void
181      send(Queue queue, Message message) throws JMSException;
182   
183   
184      /** Sends a message to a queue for an unidentified message producer, 
185        * specifying delivery mode, priority and time to live.
186        *  
187        * <P>Typically, a message producer is assigned a queue at creation 
188        * time; however, the JMS API also supports unidentified message producers,
189        * which require that the queue be supplied every time a message is
190        * sent.
191        *  
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSender.java
      * Line Number: 206
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
196        * @param timeToLive the message's lifetime (in milliseconds)
197        *  
198        * @exception JMSException if the JMS provider fails to send the message 
199        *                         due to some internal error.
200        * @exception MessageFormatException if an invalid message is specified.
201        * @exception InvalidDestinationException if a client uses
202        *                         this method with an invalid queue.
203        */ 
204  
205      void
206      send(Queue queue, 
207  	 Message message, 
208  	 int deliveryMode, 
209  	 int priority,
210  	 long timeToLive) throws JMSException;
211  }

```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 105
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
 95        * {@code createTemporaryQueue} method.
 96        *
 97        * @param queueName the name of this {@code Queue}
 98        *
 99        * @return a {@code Queue} with the given name
100        *
101        * @exception JMSException if the session fails to create a queue
102        *                         due to some internal error.
103        */ 
104   
105      Queue
106      createQueue(String queueName) throws JMSException;
107  
108  
109      /** Creates a {@code QueueReceiver} object to receive messages from the
110        * specified queue.
111        *
112        * @param queue the {@code Queue} to access
113        *
114        * @exception JMSException if the session fails to create a receiver
115        *                         due to some internal error.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 120
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
110        * specified queue.
111        *
112        * @param queue the {@code Queue} to access
113        *
114        * @exception JMSException if the session fails to create a receiver
115        *                         due to some internal error.
116        * @exception InvalidDestinationException if an invalid queue is specified.
117        */
118  
119      QueueReceiver
120      createReceiver(Queue queue) throws JMSException;
121  
122  
123      /** Creates a {@code QueueReceiver} object to receive messages from the 
124        * specified queue using a message selector.
125        *  
126        * @param queue the {@code Queue} to access
127        * @param messageSelector only messages with properties matching the
128        * message selector expression are delivered. A value of null or
129        * an empty string indicates that there is no message selector 
130        * for the message consumer.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 140
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
130        * for the message consumer.
131        *  
132        * @exception JMSException if the session fails to create a receiver
133        *                         due to some internal error.
134        * @exception InvalidDestinationException if an invalid queue is specified.
135        * @exception InvalidSelectorException if the message selector is invalid.
136        *
137        */ 
138  
139      QueueReceiver
140      createReceiver(Queue queue, 
141  		   String messageSelector) throws JMSException;
142  
143  
144      /** Creates a {@code QueueSender} object to send messages to the 
145        * specified queue.
146        *
147        * @param queue the {@code Queue} to access, or null if this is an 
148        * unidentified producer
149        *
150        * @exception JMSException if the session fails to create a sender
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 156
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
146        *
147        * @param queue the {@code Queue} to access, or null if this is an 
148        * unidentified producer
149        *
150        * @exception JMSException if the session fails to create a sender
151        *                         due to some internal error.
152        * @exception InvalidDestinationException if an invalid queue is specified.
153        */
154   
155      QueueSender
156      createSender(Queue queue) throws JMSException;
157  
158  
159      /** Creates a {@code QueueBrowser} object to peek at the messages on 
160        * the specified queue.
161        *
162        * @param queue the {@code Queue} to access
163        *
164        * @exception JMSException if the session fails to create a browser
165        *                         due to some internal error.
166        * @exception InvalidDestinationException if an invalid queue is specified.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 170
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
160        * the specified queue.
161        *
162        * @param queue the {@code Queue} to access
163        *
164        * @exception JMSException if the session fails to create a browser
165        *                         due to some internal error.
166        * @exception InvalidDestinationException if an invalid queue is specified.
167        */
168  
169      QueueBrowser 
170      createBrowser(Queue queue) throws JMSException;
171  
172  
173      /** Creates a {@code QueueBrowser} object to peek at the messages on 
174        * the specified queue using a message selector.
175        *  
176        * @param queue the {@code Queue} to access
177        * @param messageSelector only messages with properties matching the
178        * message selector expression are delivered. A value of null or
179        * an empty string indicates that there is no message selector 
180        * for the message consumer.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/QueueSession.java
      * Line Number: 189
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
179        * an empty string indicates that there is no message selector 
180        * for the message consumer.
181        *  
182        * @exception JMSException if the session fails to create a browser
183        *                         due to some internal error.
184        * @exception InvalidDestinationException if an invalid queue is specified.
185        * @exception InvalidSelectorException if the message selector is invalid.
186        */ 
187  
188      QueueBrowser
189      createBrowser(Queue queue,
190  		  String messageSelector) throws JMSException;
191  
192  
193      /** Creates a {@code TemporaryQueue} object. Its lifetime will be that 
194        * of the {@code QueueConnection} unless it is deleted earlier.
195        *
196        * @return a temporary queue identity
197        *
198        * @exception JMSException if the session fails to create a temporary queue
199        *                         due to some internal error.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TemporaryQueue.java
      * Line Number: 63
      * Message: 'JMS `Queue`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Queue to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/queue/HELLOWORLDMDBQueue")
 private Queue queue;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBQueue")
 Emitter<String> queueEmitter;
 ```'
      * Code Snippet:
```java
53    * be able participate in transactions with objects from the PTP domain.
54    *
55    * @see Session#createTemporaryQueue()
56    * @see QueueSession#createTemporaryQueue()
57    * 
58    * @version JMS 2.0
59    * @since JMS 1.0
60    * 
61    */
62  
63  public interface TemporaryQueue extends Queue {
64  
65      /** Deletes this temporary queue. If there are existing receivers
66        * still using it, a {@code JMSException} will be thrown.
67        *  
68        * @exception JMSException if the JMS provider fails to delete the 
69        *                         temporary queue due to some internal error.
70        */
71  
72      void 
73      delete() throws JMSException; 
```
### #15 - jms-to-reactive-quarkus-00040
* Category: mandatory
* Effort: 3
* Description: JMS' Topic must be replaced with an Emitter
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Emitter (Microprofile Reactive Streams Messaging): https://smallrye.io/smallrye-reactive-messaging/2.0.2/apidocs/org/eclipse/microprofile/reactive/messaging/Emitter.html
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 8
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.util.logging.Logger;
 4  import javax.ejb.Stateless;
 5  import javax.annotation.Resource;
 6  import javax.inject.Inject;
 7  import javax.jms.JMSContext;
 8  import javax.jms.Topic;
 9  
10  import com.redhat.coolstore.model.ShoppingCart;
11  import com.redhat.coolstore.utils.Transformers;
12  
13  @Stateless
14  public class ShoppingCartOrderProcessor  {
15  
16      @Inject
17      Logger log;
18  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 24
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
14  public class ShoppingCartOrderProcessor  {
15  
16      @Inject
17      Logger log;
18  
19  
20      @Inject
21      private transient JMSContext context;
22  
23      @Resource(lookup = "java:/topic/orders")
24      private Topic ordersTopic;
25  
26      
27    
28      public void  process(ShoppingCart cart) {
29          log.info("Sending order from processor: ");
30          context.createProducer().send(ordersTopic, Transformers.shoppingCartToJson(cart));
31      }
32  
33  
34  
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1022
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1012  	 * which is done using the {@code createTemporaryTopic} method.
1013  	 * 
1014  	 * @param topicName
1015  	 *            A provider-specific topic name
1016  	 * @return a Topic object which encapsulates the specified name
1017  	 * 
1018  	 * @throws JMSRuntimeException
1019  	 *             if a Topic object cannot be created due to some internal
1020  	 *             error
1021  	 */
1022  	Topic createTopic(String topicName);
1023  
1024  	/**
1025  	 * Creates an unshared durable subscription on the specified topic (if one
1026  	 * does not already exist) and creates a consumer on that durable
1027  	 * subscription. This method creates the durable subscription without a
1028  	 * message selector and with a {@code noLocal} value of {@code false}.
1029  	 * <p>
1030  	 * A durable subscription is used by an application which needs to receive
1031  	 * all the messages published on a topic, including the ones published when
1032  	 * there is no active consumer associated with it. The JMS provider retains
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1103
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
11   * https://glassfish.dev.java.net/public/CDDL+GPL_1_1.html
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1207
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1197   	 *                if an unshared durable subscription already exists with
1198   	 *                the same name and client identifier, and there is a
1199   	 *                consumer already active 
1200   	 *                <li>if a shared durable
1201   	 *                subscription already exists with the same name and client
1202   	 *                identifier
1203   	 *                </ul>
1204   	 * 
1205  	 * @since JMS 2.0
1206  	 */ 
1207        JMSConsumer createDurableConsumer(Topic topic, String name, String messageSelector, boolean noLocal);     
1208  
1209     	/**
1210     	 * Creates a shared durable subscription on the specified topic (if one
1211     	 * does not already exist), specifying a message selector,
1212     	 * and creates a consumer on that durable subscription.
1213     	 * This method creates the durable subscription without a message selector. 
1214     	 * <p>
1215  	 * A durable subscription is used by an application which needs to receive
1216  	 * all the messages published on a topic, including the ones published when
1217  	 * there is no active consumer associated with it. The JMS provider retains
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1291
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1281     	 *                the same name and client identifier, but a different topic,
1282     	 *                or message selector,
1283     	 *                and there is a consumer already active 
1284     	 *                <li>if an unshared durable
1285     	 *                subscription already exists with the same name and client
1286     	 *                identifier
1287     	 *                </ul>
1288     	 *
1289       * @since JMS 2.0
1290     	 */
1291       JMSConsumer createSharedDurableConsumer(Topic topic, String name);
1292  
1293   	/**
1294   	 * Creates a shared durable subscription on the specified topic (if one
1295   	 * does not already exist), specifying a message selector,
1296   	 * and creates a consumer on that durable subscription.
1297     	 * <p>
1298  	 * A durable subscription is used by an application which needs to receive
1299  	 * all the messages published on a topic, including the ones published when
1300  	 * there is no active consumer associated with it. The JMS provider retains
1301  	 * a record of this durable subscription and ensures that all messages from
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1379
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1369   	 *                or message selector,
1370   	 *                and there is a consumer already active 
1371   	 *                <li>if an unshared durable
1372   	 *                subscription already exists with the same name and client
1373   	 *                identifier
1374   	 *                </ul>
1375  
1376   	 *
1377     * @since JMS 2.0
1378   	 */
1379        JMSConsumer createSharedDurableConsumer(Topic topic, String name, String messageSelector);         
1380        
1381    	/**
1382    	 * Creates a shared non-durable subscription with the specified name on the
1383    	 * specified topic (if one does not already exist) and creates a consumer on
1384    	 * that subscription. This method creates the non-durable subscription
1385    	 * without a message selector.
1386    	 * <p>
1387    	 * If a shared non-durable subscription already exists with the same name
1388    	 * and client identifier (if set), and the same topic and message selector 
1389    	 * has been specified, then this method creates a
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1431
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1421  	 * 
1422  	 * @throws JMSRuntimeException
1423  	 *             if the session fails to create the shared non-durable
1424  	 *             subscription and {@code JMSContext} due to some internal
1425  	 *             error.
1426  	 * @throws InvalidDestinationRuntimeException
1427  	 *             if an invalid topic is specified.
1428  	 * @throws InvalidSelectorRuntimeException
1429  	 *             if the message selector is invalid.
1430  	 */
1431  	JMSConsumer createSharedConsumer(Topic topic, String sharedSubscriptionName);
1432  
1433  	/**
1434  	 * Creates a shared non-durable subscription with the specified name on the
1435  	 * specified topic (if one does not already exist) specifying a message selector,
1436  	 * and creates a consumer on that subscription. 
1437  	 * <p>
1438  	 * If a shared non-durable subscription already exists with the same name
1439  	 * and client identifier (if set), and the same topic and message selector 
1440  	 * has been specified, then this method creates a
1441  	 * {@code JMSConsumer} on the existing subscription.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/JMSContext.java
      * Line Number: 1487
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
1477  	 * 
1478  	 * @throws JMSRuntimeException
1479  	 *             if the session fails to create the shared non-durable
1480  	 *             subscription and {@code JMSConsumer} due to some
1481  	 *             internal error.
1482  	 * @throws InvalidDestinationRuntimeException
1483  	 *             if an invalid topic is specified.
1484  	 * @throws InvalidSelectorRuntimeException
1485  	 *             if the message selector is invalid.
1486  	 */
1487  	JMSConsumer createSharedConsumer(Topic topic, String sharedSubscriptionName, java.lang.String messageSelector);
1488  
1489  	/**
1490  	 * Creates a {@code QueueBrowser} object to peek at the messages on the
1491  	 * specified queue.
1492  	 * 
1493  	 * @param queue
1494  	 *            the {@code queue} to access
1495  	 * 
1496  	 * 
1497  	 * @exception JMSRuntimeException
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TemporaryTopic.java
      * Line Number: 64
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
54    * be able participate in transactions with objects from the Pub/Sub domain.
55    *
56    * @see Session#createTemporaryTopic()
57    * @see TopicSession#createTemporaryTopic()
58    * 
59    * @version JMS 2.0
60    * @since JMS 1.0
61    * 
62    */
63  
64  public interface TemporaryTopic extends Topic {
65  
66      /** Deletes this temporary topic. If there are existing subscribers
67        * still using it, a {@code JMSException} will be thrown.
68        *  
69        * @exception JMSException if the JMS provider fails to delete the
70        *                         temporary topic due to some internal error.
71        */
72  
73      void 
74      delete() throws JMSException; 
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/Topic.java
      * Line Number: 81
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
71    *
72    * @see        Session#createConsumer(Destination)
73    * @see        Session#createProducer(Destination)
74    * @see        javax.jms.TopicSession#createTopic(String)
75    * 
76    * @version JMS 2.0
77    * @since JMS 1.0
78    * 
79    */
80  
81  public interface Topic extends Destination {
82  
83      /** Gets the name of this topic.
84        *  
85        * <P>Clients that depend upon the name are not portable.
86        *  
87        * @return the topic name
88        *  
89        * @exception JMSException if the JMS provider implementation of 
90        *                         {@code Topic} fails to return the topic
91        *                         name due to some internal
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicConnection.java
      * Line Number: 121
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
111        *                         to create a connection consumer due to some
112        *                         internal error or invalid arguments for 
113        *                         {@code sessionPool} and 
114        *                         {@code messageSelector}.
115        * @exception InvalidDestinationException if an invalid topic is specified.
116        * @exception InvalidSelectorException if the message selector is invalid.
117        * @see javax.jms.ConnectionConsumer
118        */ 
119  
120      ConnectionConsumer
121      createConnectionConsumer(Topic topic,
122                               String messageSelector,
123                               ServerSessionPool sessionPool,
124  			     int maxMessages)
125  			     throws JMSException;
126  
127  
128      /** Create a durable connection consumer for this connection (optional operation). 
129        * This is an expert facility not used by regular JMS clients.
130        *                
131        * @param topic the topic to access
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicConnection.java
      * Line Number: 155
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
145        *                         to create a connection consumer due to some
146        *                         internal error or invalid arguments for 
147        *                         {@code sessionPool} and 
148        *                         {@code messageSelector}.
149        * @exception InvalidDestinationException if an invalid topic is specified.
150        * @exception InvalidSelectorException if the message selector is invalid.
151        * @see javax.jms.ConnectionConsumer
152        */
153  
154      ConnectionConsumer
155      createDurableConnectionConsumer(Topic topic,
156  				    String subscriptionName,
157                                      String messageSelector,
158                                      ServerSessionPool sessionPool,
159  				    int maxMessages)
160                               throws JMSException;
161  }

```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicPublisher.java
      * Line Number: 112
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
102  
103      /** Gets the topic associated with this {@code TopicPublisher}.
104        *
105        * @return this publisher's topic
106        *  
107        * @exception JMSException if the JMS provider fails to get the topic for
108        *                         this {@code TopicPublisher}
109        *                         due to some internal error.
110        */
111  
112      Topic 
113      getTopic() throws JMSException;
114  
115   
116      /** Publishes a message to the topic.
117        * Uses the {@code TopicPublisher}'s default delivery mode, priority,
118        * and time to live.
119        *
120        * @param message the message to publish
121        *
122        * @exception JMSException if the JMS provider fails to publish the message
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicPublisher.java
      * Line Number: 191
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
181        * @exception MessageFormatException if an invalid message is specified.
182        * @exception InvalidDestinationException if a client uses
183        *                         this method with an invalid topic.
184        * 
185        * @see javax.jms.MessageProducer#getDeliveryMode()
186        * @see javax.jms.MessageProducer#getTimeToLive()
187        * @see javax.jms.MessageProducer#getPriority()
188        */ 
189  
190      void
191      publish(Topic topic, Message message) throws JMSException;
192  
193  
194      /** Publishes a message to a topic for an unidentified message 
195        * producer, specifying delivery mode, priority and time to live.
196        *  
197        * <P>Typically, a message producer is assigned a topic at creation
198        * time; however, the JMS API also supports unidentified message producers,
199        * which require that the topic be supplied every time a message is
200        * published.
201        *
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicPublisher.java
      * Line Number: 216
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
206        * @param timeToLive the message's lifetime (in milliseconds)
207        *  
208        * @exception JMSException if the JMS provider fails to publish the message
209        *                         due to some internal error.
210        * @exception MessageFormatException if an invalid message is specified.
211        * @exception InvalidDestinationException if a client uses
212        *                         this method with an invalid topic.
213        */ 
214  
215      void
216      publish(Topic topic, 
217              Message message, 
218              int deliveryMode, 
219              int priority,
220  	    long timeToLive) throws JMSException;
221  }

```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicRequestor.java
      * Line Number: 88
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
78        * @param session the {@code TopicSession} the topic belongs to
79        * @param topic the topic to perform the request/reply call on
80        *
81        * @exception JMSException if the JMS provider fails to create the
82        *                         {@code TopicRequestor} due to some internal
83        *                         error.
84        * @exception InvalidDestinationException if an invalid topic is specified.
85        */ 
86  
87      public 
88      TopicRequestor(TopicSession session, Topic topic) throws JMSException {
89      	
90      	if (topic==null) throw new InvalidDestinationException("topic==null");
91  
92  	    this.session = session;
93          tempTopic    = session.createTemporaryTopic();
94          publisher    = session.createPublisher(topic);
95          subscriber   = session.createSubscriber(tempTopic);
96      }
97  
98  
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 99
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
 89        * {@code createTemporaryTopic} method.
 90        *  
 91        * @param topicName the name of this {@code Topic}
 92        *
 93        * @return a {@code Topic} with the given name
 94        *
 95        * @exception JMSException if the session fails to create a topic
 96        *                         due to some internal error.
 97        */
 98  
 99      Topic
100      createTopic(String topicName) throws JMSException;
101  
102  
103      /** Creates a nondurable subscriber to the specified topic.
104        *  
105        * <P>A client uses a {@code TopicSubscriber} object to receive 
106        * messages that have been published to a topic.
107        *
108        * <P>Regular {@code TopicSubscriber} objects are not durable. 
109        * They receive only messages that are published while they are active.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 124
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
114        * The default value for this attribute is false.
115        *
116        * @param topic the {@code Topic} to subscribe to
117        *  
118        * @exception JMSException if the session fails to create a subscriber
119        *                         due to some internal error.
120        * @exception InvalidDestinationException if an invalid topic is specified.
121        */ 
122  
123      TopicSubscriber
124      createSubscriber(Topic topic) throws JMSException;
125  
126  
127      /** Creates a nondurable subscriber to the specified topic, using a
128        * message selector or specifying whether messages published by its
129        * own connection should be delivered to it.
130        *
131        * <P>A client uses a {@code TopicSubscriber} object to receive 
132        * messages that have been published to a topic.
133        *  
134        * <P>Regular {@code TopicSubscriber} objects are not durable. 
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 161
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
151        * @param noLocal if set, inhibits the delivery of messages published
152        * by its own connection
153        * 
154        * @exception JMSException if the session fails to create a subscriber
155        *                         due to some internal error.
156        * @exception InvalidDestinationException if an invalid topic is specified.
157        * @exception InvalidSelectorException if the message selector is invalid.
158        */
159  
160      TopicSubscriber 
161      createSubscriber(Topic topic, 
162  		     String messageSelector,
163  		     boolean noLocal) throws JMSException;
164  
165  
166  	/**
167  	 * Creates an unshared durable subscription on the specified topic (if one
168  	 * does not already exist) and creates a consumer on that durable
169  	 * subscription. 
170    	 * This method creates the durable subscription without a message selector 
171    	 * and with a {@code noLocal} value of {@code false}. 
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 253
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
243  	 *                <li>if the client identifier is unset 
244  	 *                <li>
245  	 *                if an unshared durable subscription already exists with
246  	 *                the same name and client identifier, and there is a
247  	 *                consumer already active 
248  	 *                <li>if a shared durable subscription already exists 
249  	 *                with the same name and client identifier
250  	 *                </ul>
251  	 *
252  	 */
253      TopicSubscriber createDurableSubscriber(Topic topic, 
254  			    String name) throws JMSException;
255  
256  	/**
257  	 * Creates an unshared durable subscription on the specified topic (if one
258  	 * does not already exist), specifying a message selector and the
259  	 * {@code noLocal} parameter, and creates a consumer on that durable
260  	 * subscription.
261  	 * <p>
262  	 * A durable subscription is used by an application which needs to receive
263  	 * all the messages published on a topic, including the ones published when
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 359
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
349  	 *                <li>
350  	 *                if an unshared durable subscription already exists with
351  	 *                the same name and client identifier, and there is a
352  	 *                consumer already active 
353  	 *                <li>if a shared durable
354  	 *                subscription already exists with the same name and client
355  	 *                identifier
356  	 *                </ul>
357  	 *                
358  	 */
359  	TopicSubscriber createDurableSubscriber(Topic topic, String name, String messageSelector, boolean noLocal)
360  			throws JMSException;
361  
362      /** Creates a publisher for the specified topic.
363        *
364        * <P>A client uses a {@code TopicPublisher} object to publish 
365        * messages on a topic.
366        * Each time a client creates a {@code TopicPublisher} on a topic, it
367        * defines a 
368        * new sequence of messages that have no ordering relationship with the 
369        * messages it has previously sent.
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSession.java
      * Line Number: 380
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
370        *
371        * @param topic the {@code Topic} to publish to, or null if this is an
372        * unidentified producer
373        *
374        * @exception JMSException if the session fails to create a publisher
375        *                         due to some internal error.
376        * @exception InvalidDestinationException if an invalid topic is specified.
377       */
378  
379      TopicPublisher 
380      createPublisher(Topic topic) throws JMSException;
381  
382  
383      /** Creates a {@code TemporaryTopic} object. Its lifetime will be that 
384        * of the {@code TopicConnection} unless it is deleted earlier.
385        *
386        * @return a temporary topic identity
387        *
388        * @exception JMSException if the session fails to create a temporary
389        *                         topic due to some internal error.
390        */
```
  * file:///root/.m2/repository/javax/javaee-api/7.0/javax/jms/TopicSubscriber.java
      * Line Number: 122
      * Message: 'JMS `Topic`s should be replaced with Micrometer `Emitter`s feeding a Channel. See the following example of migrating
 a Topic to an Emitter:
 
 Before:
 ```
 @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
 private Topic topic;
 ```
 
 After:
 ```
 @Inject
 @Channel("HELLOWORLDMDBTopic")
 Emitter<String> topicEmitter;
 ```'
      * Code Snippet:
```java
112  
113      /** Gets the {@code Topic} associated with this subscriber.
114        *  
115        * @return this subscriber's {@code Topic}
116        *  
117        * @exception JMSException if the JMS provider fails to get the topic for
118        *                         this topic subscriber
119        *                         due to some internal error.
120        */ 
121  
122      Topic
123      getTopic() throws JMSException;
124  
125  
126      /** Gets the {@code NoLocal} attribute for this subscriber. 
127        * The default value for this attribute is false.
128        *  
129        * @return true if locally published messages are being inhibited
130        *  
131        * @exception JMSException if the JMS provider fails to get the
132        *                         {@code NoLocal} attribute for
```
### #16 - jms-to-reactive-quarkus-00050
* Category: mandatory
* Effort: 5
* Description: JMS is not supported in Quarkus
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java
      * Line Number: 7
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import com.redhat.coolstore.model.Order;
 4  import com.redhat.coolstore.utils.Transformers;
 5  
 6  import javax.inject.Inject;
 7  import javax.jms.*;
 8  import javax.naming.Context;
 9  import javax.naming.InitialContext;
10  import javax.naming.NamingException;
11  import javax.rmi.PortableRemoteObject;
12  import java.util.Hashtable;
13  
14  public class InventoryNotificationMDB implements MessageListener {
15  
16      private static final int LOW_THRESHOLD = 50;
17  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 6
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import javax.ejb.ActivationConfigProperty;
 4  import javax.ejb.MessageDriven;
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 7
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import javax.ejb.ActivationConfigProperty;
 4  import javax.ejb.MessageDriven;
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 8
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import javax.ejb.ActivationConfigProperty;
 4  import javax.ejb.MessageDriven;
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 9
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import javax.ejb.ActivationConfigProperty;
 4  import javax.ejb.MessageDriven;
 5  import javax.inject.Inject;
 6  import javax.jms.JMSException;
 7  import javax.jms.Message;
 8  import javax.jms.MessageListener;
 9  import javax.jms.TextMessage;
10  
11  import com.redhat.coolstore.model.Order;
12  import com.redhat.coolstore.utils.Transformers;
13  
14  @MessageDriven(name = "OrderServiceMDB", activationConfig = {
15  	@ActivationConfigProperty(propertyName = "destinationLookup", propertyValue = "topic/orders"),
16  	@ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Topic"),
17  	@ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge")})
18  public class OrderServiceMDB implements MessageListener { 
19  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 7
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.util.logging.Logger;
 4  import javax.ejb.Stateless;
 5  import javax.annotation.Resource;
 6  import javax.inject.Inject;
 7  import javax.jms.JMSContext;
 8  import javax.jms.Topic;
 9  
10  import com.redhat.coolstore.model.ShoppingCart;
11  import com.redhat.coolstore.utils.Transformers;
12  
13  @Stateless
14  public class ShoppingCartOrderProcessor  {
15  
16      @Inject
17      Logger log;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 8
      * Message: 'References to JavaEE/JakartaEE JMS elements should be removed and replaced with their Quarkus SmallRye/Microprofile equivalents.'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.util.logging.Logger;
 4  import javax.ejb.Stateless;
 5  import javax.annotation.Resource;
 6  import javax.inject.Inject;
 7  import javax.jms.JMSContext;
 8  import javax.jms.Topic;
 9  
10  import com.redhat.coolstore.model.ShoppingCart;
11  import com.redhat.coolstore.utils.Transformers;
12  
13  @Stateless
14  public class ShoppingCartOrderProcessor  {
15  
16      @Inject
17      Logger log;
18  
```
### #17 - persistence-to-quarkus-00000
* Category: optional
* Effort: 1
* Description: Move persistence config to a properties file
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Using Hibernate ORM and Jakarta persistence: https://quarkus.io/guides/hibernate-orm#persistence-xml
* Incidents
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: -1
      * Message: 'It is recommended to move persistence related configuration from an XML file to a properties one.
 This allows centralization of the configuration in Quarkus. Check the link for more information.
 
 
 Datasource and persistence configurations in XML can be substituted with a single centralized properties file. Here is an example of a translation:
 
 The following datasource configuration:
 ```
 <datasources xmlns="http://www.jboss.org/ironjacamar/schema"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.jboss.org/ironjacamar/schema http://docs.jboss.org/ironjacamar/schema/datasources_1_0.xsd">
 <!-- The datasource is bound into JNDI at this location. We reference
 this in META-INF/persistence.xml -->
 <datasource jndi-name="java:jboss/datasources/TasksJsfQuickstartDS"
 pool-name="tasks-jsf-quickstart" enabled="true"
 use-java-context="true">
 <connection-url>jdbc:h2:mem:tasks-jsf-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1</connection-url>
 <driver>h2</driver>
 <security>
 <user-name>sa</user-name>
 <password>sa</password>
 </security>
 </datasource>
 </datasources>
 ```
 along with the following persistence configuration:
 ```
 <persistence version="2.1"
 xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="
 http://xmlns.jcp.org/xml/ns/persistence
 http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
 <persistence-unit name="primary">
 <!-- We use a different datasource for tests, so as to not overwrite
 production data. This is an unmanaged data source, backed by H2, an in memory
 database. Production applications should use a managed datasource. -->
 <!-- The datasource is deployed as WEB-INF/test-ds.xml,
 you can find it in the source at src/test/resources/test-ds.xml -->
 <jta-data-source>java:jboss/datasources/TasksJsfQuickstartDS</jta-data-source>
 <properties>
 <!-- Properties for Hibernate -->
 <property name="hibernate.hbm2ddl.auto" value="create-drop" />
 <property name="hibernate.show_sql" value="false" />
 </properties>
 </persistence-unit>
 </persistence>
 ```
 can be translated to:
 ```
 quarkus.datasource.jdbc.url=jdbc:h2:mem:tasks-jsf-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1
 quarkus.datasource.db-kind=h2
 quarkus.datasource.username=sa
 quarkus.datasource.password=sa

 quarkus.hibernate-orm.database.generation=drop-and-create
 ```'
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: -1
      * Message: 'It is recommended to move persistence related configuration from an XML file to a properties one.
 This allows centralization of the configuration in Quarkus. Check the link for more information.
 
 
 Datasource and persistence configurations in XML can be substituted with a single centralized properties file. Here is an example of a translation:
 
 The following datasource configuration:
 ```
 <datasources xmlns="http://www.jboss.org/ironjacamar/schema"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.jboss.org/ironjacamar/schema http://docs.jboss.org/ironjacamar/schema/datasources_1_0.xsd">
 <!-- The datasource is bound into JNDI at this location. We reference
 this in META-INF/persistence.xml -->
 <datasource jndi-name="java:jboss/datasources/TasksJsfQuickstartDS"
 pool-name="tasks-jsf-quickstart" enabled="true"
 use-java-context="true">
 <connection-url>jdbc:h2:mem:tasks-jsf-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1</connection-url>
 <driver>h2</driver>
 <security>
 <user-name>sa</user-name>
 <password>sa</password>
 </security>
 </datasource>
 </datasources>
 ```
 along with the following persistence configuration:
 ```
 <persistence version="2.1"
 xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="
 http://xmlns.jcp.org/xml/ns/persistence
 http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
 <persistence-unit name="primary">
 <!-- We use a different datasource for tests, so as to not overwrite
 production data. This is an unmanaged data source, backed by H2, an in memory
 database. Production applications should use a managed datasource. -->
 <!-- The datasource is deployed as WEB-INF/test-ds.xml,
 you can find it in the source at src/test/resources/test-ds.xml -->
 <jta-data-source>java:jboss/datasources/TasksJsfQuickstartDS</jta-data-source>
 <properties>
 <!-- Properties for Hibernate -->
 <property name="hibernate.hbm2ddl.auto" value="create-drop" />
 <property name="hibernate.show_sql" value="false" />
 </properties>
 </persistence-unit>
 </persistence>
 ```
 can be translated to:
 ```
 quarkus.datasource.jdbc.url=jdbc:h2:mem:tasks-jsf-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1
 quarkus.datasource.db-kind=h2
 quarkus.datasource.username=sa
 quarkus.datasource.password=sa

 quarkus.hibernate-orm.database.generation=drop-and-create
 ```'
### #18 - persistence-to-quarkus-00011
* Category: potential
* Effort: 1
* Description: @Produces cannot annotate an EntityManager
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Setting up and configuring Hibernate ORM: https://quarkus.io/guides/hibernate-orm#setting-up-and-configuring-hibernate-orm
  * Using Hibernate ORM and Jakarta persistence: https://quarkus.io/guides/hibernate-orm#persistence-xml
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 5
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource, so the `@PersistenceContext` annotation can be removed. 
This also makes having a `@Produces` annotation
 on the `EntityManager` illegal in Quarkus.
 
 If you are using a `@Produces` annotation for your EntityManager, and it is not needed after configuring your datasource, remove it and `@Inject` the EntityManager.
 Otherwise, if the producer is still needed, please create a qualification for your produced `EntityManager`, as well as every injection point for the EM.
 
 For instance, you can create an `ExtendedContext` qualifier:
 ```
 @Qualifier
 @Target()
 @Retention(RetentionPolicy.RUNTIME)
 public @interface ExtendedContext 
 ```
 and then inject your entity managers:
 ```
 @ExtendedContext
 public EntityManager getEm() 
 ```'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.persistence;
 2  
 3  import javax.enterprise.context.Dependent;
 4  import javax.enterprise.inject.Produces;
 5  import javax.persistence.EntityManager;
 6  import javax.persistence.PersistenceContext;
 7  
 8  @Dependent
 9  public class Resources {
10  
11      @PersistenceContext
12      private EntityManager em;
13  
14      @Produces
15      public EntityManager getEntityManager() {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 13
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource, so the `@PersistenceContext` annotation can be removed. 
This also makes having a `@Produces` annotation
 on the `EntityManager` illegal in Quarkus.
 
 If you are using a `@Produces` annotation for your EntityManager, and it is not needed after configuring your datasource, remove it and `@Inject` the EntityManager.
 Otherwise, if the producer is still needed, please create a qualification for your produced `EntityManager`, as well as every injection point for the EM.
 
 For instance, you can create an `ExtendedContext` qualifier:
 ```
 @Qualifier
 @Target()
 @Retention(RetentionPolicy.RUNTIME)
 public @interface ExtendedContext 
 ```
 and then inject your entity managers:
 ```
 @ExtendedContext
 public EntityManager getEm() 
 ```'
      * Code Snippet:
```java
 3  import java.util.List;
 4  import java.util.logging.Logger;
 5  
 6  import javax.inject.Inject;
 7  
 8  import javax.persistence.criteria.CriteriaBuilder;
 9  import javax.persistence.criteria.CriteriaQuery;
10  import javax.persistence.criteria.Root;
11  
12  import javax.ejb.Stateless;
13  import javax.persistence.EntityManager;
14  
15  import com.redhat.coolstore.model.*;
16  
17  @Stateless
18  public class CatalogService {
19  
20      @Inject
21      Logger log;
22  
23      @Inject
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 7
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource, so the `@PersistenceContext` annotation can be removed. 
This also makes having a `@Produces` annotation
 on the `EntityManager` illegal in Quarkus.
 
 If you are using a `@Produces` annotation for your EntityManager, and it is not needed after configuring your datasource, remove it and `@Inject` the EntityManager.
 Otherwise, if the producer is still needed, please create a qualification for your produced `EntityManager`, as well as every injection point for the EM.
 
 For instance, you can create an `ExtendedContext` qualifier:
 ```
 @Qualifier
 @Target()
 @Retention(RetentionPolicy.RUNTIME)
 public @interface ExtendedContext 
 ```
 and then inject your entity managers:
 ```
 @ExtendedContext
 public EntityManager getEm() 
 ```'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import com.redhat.coolstore.model.Order;
 4  import java.util.List;
 5  import javax.ejb.Stateless;
 6  import javax.inject.Inject;
 7  import javax.persistence.EntityManager;
 8  import javax.persistence.criteria.CriteriaBuilder;
 9  import javax.persistence.criteria.CriteriaQuery;
10  import javax.persistence.criteria.Root;
11  
12  @Stateless
13  public class OrderService {
14  
15    @Inject
16    private EntityManager em;
17  
```
### #19 - remote-ejb-to-quarkus-00000
* Category: mandatory
* Effort: 1
* Description: Remote EJBs are not supported in Quarkus
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 12
      * Message: 'Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:
 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path("<endpoint>")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.
 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.
 3. For every public method on the EJB being converted, do the following:
 - In case the method has no input parameters, annotate the method with `@jakarta.ws.rs.GET`; otherwise annotate it with `@jakarta.ws.rs.POST` instead.
 - Annotate the method with `@jakarta.ws.rs.Path("<endpoint>")` and give it a proper endpoint path. As a rule of thumb, the method name can be used as endpoint, for instance:
 ```
 @Path("/increment")
 public void increment() 
 ```
 - Add `@jakarta.ws.rs.QueryParam("<param-name>")` to any method parameters if needed, where `<param-name>` is a name for the parameter.'
      * Code Snippet:
```java
 2  
 3  import java.math.BigDecimal;
 4  import java.math.RoundingMode;
 5  
 6  import javax.ejb.Remote;
 7  import javax.ejb.Stateless;
 8  
 9  import com.redhat.coolstore.model.ShoppingCart;
10  
11  @Stateless
12  @Remote
13  public class ShippingService implements ShippingServiceRemote {
14  
15      @Override
16      public double calculateShipping(ShoppingCart sc) {
17  
18          if (sc != null) {
19  
20              if (sc.getCartItemTotal() >= 0 && sc.getCartItemTotal() < 25) {
21  
22                  return 2.99;
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/ejb/Remote.java
      * Line Number: 67
      * Message: 'Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:
 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path("<endpoint>")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.
 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.
 3. For every public method on the EJB being converted, do the following:
 - In case the method has no input parameters, annotate the method with `@jakarta.ws.rs.GET`; otherwise annotate it with `@jakarta.ws.rs.POST` instead.
 - Annotate the method with `@jakarta.ws.rs.Path("<endpoint>")` and give it a proper endpoint path. As a rule of thumb, the method name can be used as endpoint, for instance:
 ```
 @Path("/increment")
 public void increment() 
 ```
 - Add `@jakarta.ws.rs.QueryParam("<param-name>")` to any method parameters if needed, where `<param-name>` is a name for the parameter.'
      * Code Snippet:
```java
57   * be provided.
58   * <p>
59   * The <code>Remote</code> annotation applies only to session beans and 
60   * their interfaces.
61   *
62   * @since EJB 3.0
63   */
64  
65  @Target({ElementType.TYPE})
66  @Retention(RetentionPolicy.RUNTIME)
67  public @interface Remote {
68  
69      /**
70       * Specifies the remote business interface(s) of the bean.  The <code>value</code>
71       * element is specified only when the annotation is applied to the bean class. 
72       * It is only required to be specified if any of the following is true:
73       * <ul>
74       * <li>the bean class does not implement its remote business interface
75       * <li>at least one of the implemented interfaces is designated as a local interface
76       * <li>the bean class implements two or more interfaces and at
77       * least one of the implemented interfaces is designated
```
