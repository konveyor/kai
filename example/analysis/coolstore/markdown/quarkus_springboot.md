# quarkus/springboot
## Description
This ruleset gives hints to migrate from SpringBoot devtools to Quarkus
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 12
### #0 - cdi-to-quarkus-00030
* Category: potential
* Effort: 3
* Description: `beans.xml` descriptor content is ignored
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Incidents
  * file:///tmp/source-code/src/main/webapp/WEB-INF/beans.xml
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 14
      * Message: 'In Quarkus, you can skip the @Produces annotation completely if the producer method is annotated with a scope annotation, a stereotype or a qualifier..
 This field could be accessed using a `@Named` getter method instead.'
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
 16          return em;
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Producers.java
      * Line Number: 12
      * Message: 'In Quarkus, you can skip the @Produces annotation completely if the producer method is annotated with a scope annotation, a stereotype or a qualifier..
 This field could be accessed using a `@Named` getter method instead.'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
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
### #2 - cdi-to-quarkus-00050
* Category: potential
* Effort: 1
* Description: Stateless annotation can be replaced with scope
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus CDI reference: https://quarkus.io/guides/cdi-reference
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 17
      * Message: 'Stateless EJBs can be converted to a cdi bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.service;
  2  
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
 24      private EntityManager em;
 25  
 26      public CatalogService() {
 27      }
 28  
 29      public List<CatalogItemEntity> getCatalogItems() {
 30          CriteriaBuilder cb = em.getCriteriaBuilder();
 31          CriteriaQuery<CatalogItemEntity> criteria = cb.createQuery(CatalogItemEntity.class);
 32          Root<CatalogItemEntity> member = criteria.from(CatalogItemEntity.class);
 33          criteria.select(member);
 34          return em.createQuery(criteria).getResultList();
 35      }
 36  
 37      public CatalogItemEntity getCatalogItemById(String itemId) {
 38          return em.find(CatalogItemEntity.class, itemId);
 39      }
 40  
 41      public void updateInventoryItems(String itemId, int deducts) {
 42          InventoryEntity inventoryEntity = getCatalogItemById(itemId).getInventory();
 43          int currentQuantity = inventoryEntity.getQuantity();
 44          inventoryEntity.setQuantity(currentQuantity-deducts);
 45          em.merge(inventoryEntity);
 46      }
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 12
      * Message: 'Stateless EJBs can be converted to a cdi bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
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
 18    public void save(Order order) {
 19      em.persist(order);
 20    }
 21  
 22    public List<Order> getOrders() {
 23      CriteriaBuilder cb = em.getCriteriaBuilder();
 24      CriteriaQuery<Order> criteria = cb.createQuery(Order.class);
 25      Root<Order> member = criteria.from(Order.class);
 26      criteria.select(member);
 27      return em.createQuery(criteria).getResultList();
 28    }
 29  
 30    public Order getOrderById(long id) {
 31      return em.find(Order.class, id);
 32    }
 33  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ProductService.java
      * Line Number: 14
      * Message: 'Stateless EJBs can be converted to a cdi bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.service;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
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
 25      }
 26  
 27      public Product getProductByItemId(String itemId) {
 28          CatalogItemEntity entity = cm.getCatalogItemById(itemId);
 29          if (entity == null)
 30              return null;
 31  
 32          // Return the entity
 33          return Transformers.toProduct(entity);
 34      }
 35  
 36  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 11
      * Message: 'Stateless EJBs can be converted to a cdi bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
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
 22                  return 2.99;
 23  
 24              } else if (sc.getCartItemTotal() >= 25 && sc.getCartItemTotal() < 50) {
 25  
 26                  return 4.99;
 27  
 28              } else if (sc.getCartItemTotal() >= 50 && sc.getCartItemTotal() < 75) {
 29  
 30                  return 6.99;
 31  
 32              } else if (sc.getCartItemTotal() >= 75 && sc.getCartItemTotal() < 100) {
 33  
 34                  return 8.99;
 35  
 36              } else if (sc.getCartItemTotal() >= 100 && sc.getCartItemTotal() < 10000) {
 37  
 38                  return 10.99;
 39  
 40              }
 41  
 42          }
 43  
 44          return 0;
 45  
 46      }
 47  
 48      @Override
 49      public double calculateShippingInsurance(ShoppingCart sc) {
 50  
 51          if (sc != null) {
 52  
 53              if (sc.getCartItemTotal() >= 25 && sc.getCartItemTotal() < 100) {
 54  
 55                  return getPercentOfTotal(sc.getCartItemTotal(), 0.02);
 56  
 57              } else if (sc.getCartItemTotal() >= 100 && sc.getCartItemTotal() < 500) {
 58  
 59                  return getPercentOfTotal(sc.getCartItemTotal(), 0.015);
 60  
 61              } else if (sc.getCartItemTotal() >= 500 && sc.getCartItemTotal() < 10000) {
 62  
 63                  return getPercentOfTotal(sc.getCartItemTotal(), 0.01);
 64  
 65              }
 66  
 67          }
 68  
 69          return 0;
 70      }
 71  
 72      private static double getPercentOfTotal(double value, double percentOfTotal) {
 73          return BigDecimal.valueOf(value * percentOfTotal)
 74                  .setScale(2, RoundingMode.HALF_UP)
 75                  .doubleValue();
 76      }
 77  
 78  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 13
      * Message: 'Stateless EJBs can be converted to a cdi bean by replacing the `@Stateless` annotation with a scope eg `@ApplicationScoped`'
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
 35  }

```
### #3 - javaee-pom-to-quarkus-00010
* Category: mandatory
* Effort: 1
* Description: Adopt Quarkus BOM
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
  * Quarkus - Releases: https://quarkus.io/blog/tag/release/
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #4 - javaee-pom-to-quarkus-00020
* Category: mandatory
* Effort: 1
* Description: Adopt Quarkus Maven plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #5 - javaee-pom-to-quarkus-00030
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Compiler plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #6 - javaee-pom-to-quarkus-00040
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Surefire plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #7 - javaee-pom-to-quarkus-00050
* Category: mandatory
* Effort: 1
* Description: Adopt Maven Failsafe plugin
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #8 - javaee-pom-to-quarkus-00060
* Category: mandatory
* Effort: 1
* Description: Add Maven profile to run the Quarkus native build
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/maven-tooling#build-tool-maven
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #9 - jaxrs-to-quarkus-00020
* Category: optional
* Effort: 1
* Description: JAX-RS activation is no longer necessary
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/resteasy-reactive#declaring-endpoints-uri-mapping
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/RestApplication.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/RestApplication.java
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
### #10 - quarkus-flyway-00000
* Category: mandatory
* Effort: 1
* Description: Replace the 'flyway-core' dependency with Quarkus 'quarkus-flyway' extension
* Labels: konveyor.io/source=flyway, konveyor.io/target=quarkus
* Incidents
  * file:///tmp/source-code/pom.xml
      * Line Number: 36
      * Message: 'Replace the `org.flywaydb:flyway-core` dependency with the Quarkus dependency `io.quarkus:quarkus-flyway` 
 Further information in the link below.'
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
### #11 - quarkus-flyway-00010
* Category: mandatory
* Effort: 1
* Description: Replace the 'flyway-core' dependency with Quarkus 'quarkus-flyway' extension
* Labels: konveyor.io/source=flyway, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides/flyway
* Incidents
  * file:///tmp/source-code/pom.xml
      * Line Number: 36
      * Message: 'Replace the `org.flywaydb:flyway-core` dependency with the Quarkus dependency `io.quarkus:quarkus-flyway` 
 Further information in the link below.'
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
