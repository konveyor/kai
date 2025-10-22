# eap8/eap7
## Description
This ruleset provides analysis of Java EE applications that need to change certain CDI-related method calls.
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 12
### #0 - hibernate-00005
* Category: potential
* Effort: 3
* Description: Implicit name determination for sequences and tables associated with identifier generation has changed
* Labels: hibernate, konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8+, konveyor.io/target=hibernate, konveyor.io/target=hibernate6+, konveyor.io/target=quarkus, konveyor.io/target=quarkus3+
* Links
  * Hibernate ORM 6 migration guide - Implicit Identifier Sequence and Table Name: https://github.com/hibernate/hibernate-orm/blob/6.0/migration-guide.adoc#implicit-identifier-sequence-and-table-name
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 24
      * Message: 'The way in which Hibernate determines implicit names for sequences and tables associated with identifier generation has changed in 6.0 which may affect migrating applications. 
 As of 6.0, Hibernate by default creates a sequence per entity hierarchy instead of a single sequence hibernate_sequence. 
 Due to this change, users that previously used `@GeneratedValue(strategy = GenerationStrategy.AUTO)` or simply `@GeneratedValue` (since `AUTO` is the default), need to ensure that the database now contains sequences for every entity, named `<entity name>_seq`. For an entity Person, a sequence person_seq is expected to exist. 
 It’s best to run hbm2ddl (e.g. by temporarily setting `hbm2ddl.auto=create`) to obtain a list of DDL statements for the sequences.'
      * Code Snippet:
```java
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
22  
23  	@Id
24  	@GeneratedValue
25  	private long orderId;
26  
27  	private String customerName;
28  
29  	private String customerEmail;
30  
31  	private double orderValue;
32  
33  	private double retailPrice;
34  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 18
      * Message: 'The way in which Hibernate determines implicit names for sequences and tables associated with identifier generation has changed in 6.0 which may affect migrating applications. 
 As of 6.0, Hibernate by default creates a sequence per entity hierarchy instead of a single sequence hibernate_sequence. 
 Due to this change, users that previously used `@GeneratedValue(strategy = GenerationStrategy.AUTO)` or simply `@GeneratedValue` (since `AUTO` is the default), need to ensure that the database now contains sequences for every entity, named `<entity name>_seq`. For an entity Person, a sequence person_seq is expected to exist. 
 It’s best to run hbm2ddl (e.g. by temporarily setting `hbm2ddl.auto=create`) to obtain a list of DDL statements for the sequences.'
      * Code Snippet:
```java
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
16  	@Id
17  	@Column(name="ID")
18  	@GeneratedValue
19  	private long id;
20  
21  	private int quantity;
22  
23  	private String productId;
24  
25  	public OrderItem() {}
26  
27  	public String getProductId() {
28  		return productId;
```
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/persistence/GeneratedValue.java
      * Line Number: 63
      * Message: 'The way in which Hibernate determines implicit names for sequences and tables associated with identifier generation has changed in 6.0 which may affect migrating applications. 
 As of 6.0, Hibernate by default creates a sequence per entity hierarchy instead of a single sequence hibernate_sequence. 
 Due to this change, users that previously used `@GeneratedValue(strategy = GenerationStrategy.AUTO)` or simply `@GeneratedValue` (since `AUTO` is the default), need to ensure that the database now contains sequences for every entity, named `<entity name>_seq`. For an entity Person, a sequence person_seq is expected to exist. 
 It’s best to run hbm2ddl (e.g. by temporarily setting `hbm2ddl.auto=create`) to obtain a list of DDL statements for the sequences.'
      * Code Snippet:
```java
53   *
54   * @see Id
55   * @see TableGenerator
56   * @see SequenceGenerator
57   *
58   * @since Java Persistence 1.0
59   */
60  @Target({METHOD, FIELD})
61  @Retention(RUNTIME)
62  
63  public @interface GeneratedValue {
64  
65      /**
66       * (Optional) The primary key generation strategy
67       * that the persistence provider must use to
68       * generate the annotated entity primary key.
69       */
70      GenerationType strategy() default AUTO;
71  
72      /**
73       * (Optional) The name of the primary key generator
```
### #1 - javaee-to-jakarta-namespaces-00001
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE namespace, schemaLocation and version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta EE XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#10
* Incidents
  * file:///opt/input/source/src/main/webapp/WEB-INF/beans.xml
      * Line Number: 18
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number'
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
  * file:///opt/input/source/src/main/webapp/WEB-INF/beans.xml
      * Line Number: 20
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number'
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
  * file:///opt/input/source/src/main/webapp/WEB-INF/beans.xml
      * Line Number: 21
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number'
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
### #2 - javaee-to-jakarta-namespaces-00002
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE persistence namespace, schemaLocation and version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta Persistence XML Schemas: https://jakarta.ee/xml/ns/persistence/#3
* Incidents
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 3
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 5
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 6
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 3
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 5
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 6
      * Message: 'Replace `http://xmlns.jcp.org/xml/ns/persistence` with `https://jakarta.ee/xml/ns/persistence` and change the schema version number'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
### #3 - javaee-to-jakarta-namespaces-00006
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE XSD with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#9
* Incidents
  * file:///opt/input/source/src/main/webapp/WEB-INF/beans.xml
      * Line Number: 21
      * Message: 'Replace `beans_1_1.xsd` with `beans_3_0.xsd` and update the version attribute to `"3.0"`'
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
### #4 - javaee-to-jakarta-namespaces-00030
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE XSD with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#9
* Incidents
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 6
      * Message: 'Replace `persistence_2_1.xsd` with `persistence_3_0.xsd` and update the version attribute to `"3.0"`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 6
      * Message: 'Replace `persistence_2_1.xsd` with `persistence_3_0.xsd` and update the version attribute to `"3.0"`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
### #5 - javaee-to-jakarta-namespaces-00033
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Incidents
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 2
      * Message: 'In the root tag, replace the `version` attribute value `2.1` with `3.0`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 8
      * Message: 'In the root tag, replace the `version` attribute value `2.1` with `3.0`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 2
      * Message: 'In the root tag, replace the `version` attribute value `2.1` with `3.0`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 8
      * Message: 'In the root tag, replace the `version` attribute value `2.1` with `3.0`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
### #6 - javax-to-jakarta-dependencies-00006
* Category: mandatory
* Effort: 1
* Description: javax groupId has been replaced by jakarta.platform
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 19
      * Message: 'Update group dependency by replacing the `javax` groupId with `jakarta.platform`'
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
  * file:///opt/input/source/pom.xml
      * Line Number: 25
      * Message: 'Update group dependency by replacing the `javax` groupId with `jakarta.platform`'
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
### #7 - javax-to-jakarta-dependencies-00007
* Category: mandatory
* Effort: 1
* Description: javax javaee-api artifactId has been replaced by jakarta.platform jakarta.jakartaee-api
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 26
      * Message: 'Update artifact dependency by replacing the `javaee-api` artifactId with `jakarta.jakartaee-api`'
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
### #8 - javax-to-jakarta-dependencies-00008
* Category: mandatory
* Effort: 1
* Description: javax javaee-web-api artifactId has been replaced by jakarta.platform jakarta.jakartaee-web-api
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///opt/input/source/pom.xml
      * Line Number: 20
      * Message: 'Update artifact dependency by replacing the `javaee-web-api` artifactId with `jakarta.jakartaee-web-api`'
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
### #9 - javax-to-jakarta-import-00001
* Category: mandatory
* Effort: 1
* Description: The package 'javax' has been replaced by 'jakarta'.
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Incidents
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 5
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 6
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
16  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 7
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
16  
17  	private static final long serialVersionUID = 7526472295622776147L; 
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 8
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
16  
17  	private static final long serialVersionUID = 7526472295622776147L; 
18  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 9
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
16  
17  	private static final long serialVersionUID = 7526472295622776147L; 
18  
19      @Id
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
      * Line Number: 10
      * Message: 'Replace the `javax.xml` import statement with `jakarta.xml`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.Id;
 8  import javax.persistence.Table;
 9  import javax.persistence.UniqueConstraint;
10  import javax.xml.bind.annotation.XmlRootElement;
11  
12  @Entity
13  @XmlRootElement
14  @Table(name = "INVENTORY", uniqueConstraints = @UniqueConstraint(columnNames = "itemId"))
15  public class InventoryEntity implements Serializable {
16  
17  	private static final long serialVersionUID = 7526472295622776147L; 
18  
19      @Id
20      private String itemId;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 7
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 8
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 9
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 10
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 11
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 12
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
22  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 13
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
22  
23  	@Id
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 14
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
22  
23  	@Id
24  	@GeneratedValue
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 15
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 5  import java.util.List;
 6  
 7  import javax.persistence.CascadeType;
 8  import javax.persistence.Column;
 9  import javax.persistence.Entity;
10  import javax.persistence.FetchType;
11  import javax.persistence.GeneratedValue;
12  import javax.persistence.Id;
13  import javax.persistence.JoinColumn;
14  import javax.persistence.OneToMany;
15  import javax.persistence.Table;
16  
17  @Entity
18  @Table(name = "ORDERS")
19  public class Order implements Serializable {
20  
21  	private static final long serialVersionUID = -1L;
22  
23  	@Id
24  	@GeneratedValue
25  	private long orderId;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 5
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.GeneratedValue;
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 6
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.GeneratedValue;
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
16  	@Id
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 7
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.GeneratedValue;
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
16  	@Id
17  	@Column(name="ID")
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 8
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.GeneratedValue;
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
16  	@Id
17  	@Column(name="ID")
18  	@GeneratedValue
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/OrderItem.java
      * Line Number: 9
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  
 5  import javax.persistence.Column;
 6  import javax.persistence.Entity;
 7  import javax.persistence.GeneratedValue;
 8  import javax.persistence.Id;
 9  import javax.persistence.Table;
10  
11  @Entity
12  @Table(name = "ORDER_ITEMS")
13  public class OrderItem implements Serializable {
14  	private static final long serialVersionUID = 64565445665456666L;
15  
16  	@Id
17  	@Column(name="ID")
18  	@GeneratedValue
19  	private long id;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/model/ShoppingCart.java
      * Line Number: 7
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.model;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.List;
 6  
 7  import javax.enterprise.context.Dependent;
 8  
 9  @Dependent
10  public class ShoppingCart implements Serializable {
11  
12  	private static final long serialVersionUID = -1108043957592113528L;
13  
14  	private double cartItemTotal;
15  
16  	private double cartItemPromoSavings;
17  	
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 3
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 4
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 5
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 6
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 9
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 10
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 11
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 12
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 2  
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 13
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 3  import java.io.Serializable;
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
23  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 14
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 4  import java.util.ArrayList;
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
23  
24  @SessionScoped
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 15
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 5  import java.util.HashMap;
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
23  
24  @SessionScoped
25  @Path("/cart")
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 16
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 6  import java.util.List;
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
23  
24  @SessionScoped
25  @Path("/cart")
26  public class CartEndpoint implements Serializable {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 17
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 7  import java.util.Map;
 8  
 9  import javax.enterprise.context.SessionScoped;
10  import javax.inject.Inject;
11  import javax.ws.rs.DELETE;
12  import javax.ws.rs.GET;
13  import javax.ws.rs.POST;
14  import javax.ws.rs.Path;
15  import javax.ws.rs.PathParam;
16  import javax.ws.rs.Produces;
17  import javax.ws.rs.core.MediaType;
18  
19  import com.redhat.coolstore.model.Product;
20  import com.redhat.coolstore.model.ShoppingCart;
21  import com.redhat.coolstore.model.ShoppingCartItem;
22  import com.redhat.coolstore.service.ShoppingCartService;
23  
24  @SessionScoped
25  @Path("/cart")
26  public class CartEndpoint implements Serializable {
27  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 6
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 7
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 8
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 9
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
19  @Path("/orders")
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 10
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
19  @Path("/orders")
20  @Consumes(MediaType.APPLICATION_JSON)
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 11
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
19  @Path("/orders")
20  @Consumes(MediaType.APPLICATION_JSON)
21  @Produces(MediaType.APPLICATION_JSON)
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 12
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
19  @Path("/orders")
20  @Consumes(MediaType.APPLICATION_JSON)
21  @Produces(MediaType.APPLICATION_JSON)
22  public class OrderEndpoint implements Serializable {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 13
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.Consumes;
 9  import javax.ws.rs.GET;
10  import javax.ws.rs.Path;
11  import javax.ws.rs.PathParam;
12  import javax.ws.rs.Produces;
13  import javax.ws.rs.core.MediaType;
14  
15  import com.redhat.coolstore.model.Order;
16  import com.redhat.coolstore.service.OrderService;
17  
18  @RequestScoped
19  @Path("/orders")
20  @Consumes(MediaType.APPLICATION_JSON)
21  @Produces(MediaType.APPLICATION_JSON)
22  public class OrderEndpoint implements Serializable {
23  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
      * Line Number: 6
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.*;
 9  import javax.ws.rs.core.MediaType;
10  
11  import com.redhat.coolstore.model.Product;
12  import com.redhat.coolstore.service.ProductService;
13  
14  @RequestScoped
15  @Path("/products")
16  @Consumes(MediaType.APPLICATION_JSON)
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
      * Line Number: 7
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.*;
 9  import javax.ws.rs.core.MediaType;
10  
11  import com.redhat.coolstore.model.Product;
12  import com.redhat.coolstore.service.ProductService;
13  
14  @RequestScoped
15  @Path("/products")
16  @Consumes(MediaType.APPLICATION_JSON)
17  @Produces(MediaType.APPLICATION_JSON)
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
      * Line Number: 9
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.rest;
 2  
 3  import java.io.Serializable;
 4  import java.util.List;
 5  
 6  import javax.enterprise.context.RequestScoped;
 7  import javax.inject.Inject;
 8  import javax.ws.rs.*;
 9  import javax.ws.rs.core.MediaType;
10  
11  import com.redhat.coolstore.model.Product;
12  import com.redhat.coolstore.service.ProductService;
13  
14  @RequestScoped
15  @Path("/products")
16  @Consumes(MediaType.APPLICATION_JSON)
17  @Produces(MediaType.APPLICATION_JSON)
18  public class ProductEndpoint implements Serializable {
19  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/rest/RestApplication.java
      * Line Number: 3
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
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
      * Line Number: 4
      * Message: 'Replace the `javax.ws` import statement with `jakarta.ws`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 12
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 6
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 8
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 9
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 10
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 13
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java
      * Line Number: 6
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 5
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 6
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 7
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 8
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 9
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderService.java
      * Line Number: 10
      * Message: 'Replace the `javax.persistence` import statement with `jakarta.persistence`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 3
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 4
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 5
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 6
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ProductService.java
      * Line Number: 7
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ProductService.java
      * Line Number: 8
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/PromoService.java
      * Line Number: 9
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.io.Serializable;
 4  import java.util.HashMap;
 5  import java.util.HashSet;
 6  import java.util.Map;
 7  import java.util.Set;
 8  
 9  import javax.enterprise.context.ApplicationScoped;
10  
11  import com.redhat.coolstore.model.Promotion;
12  import com.redhat.coolstore.model.ShoppingCart;
13  import com.redhat.coolstore.model.ShoppingCartItem;
14  
15  @ApplicationScoped
16  public class PromoService implements Serializable {
17  
18      private static final long serialVersionUID = 2088590587856645568L;
19  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 6
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 7
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 5
      * Message: 'Replace the `javax.annotation` import statement with `jakarta.annotation`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 4
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 6
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
      * Line Number: 7
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
      * Message: 'Replace the `javax.jms` import statement with `jakarta.jms`'
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
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartService.java
      * Line Number: 6
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.util.Hashtable;
 4  import java.util.logging.Logger;
 5  
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/service/ShoppingCartService.java
      * Line Number: 7
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.service;
 2  
 3  import java.util.Hashtable;
 4  import java.util.logging.Logger;
 5  
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 6
      * Message: 'Replace the `javax.annotation` import statement with `jakarta.annotation`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 7
      * Message: 'Replace the `javax.annotation` import statement with `jakarta.annotation`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 8
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
18   * Created by tqvarnst on 2017-04-04.
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 9
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
18   * Created by tqvarnst on 2017-04-04.
19   */
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 10
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
18   * Created by tqvarnst on 2017-04-04.
19   */
20  @Singleton
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 11
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
18   * Created by tqvarnst on 2017-04-04.
19   */
20  @Singleton
21  @Startup
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 12
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 2  
 3  import org.flywaydb.core.Flyway;
 4  import org.flywaydb.core.api.FlywayException;
 5  
 6  import javax.annotation.PostConstruct;
 7  import javax.annotation.Resource;
 8  import javax.ejb.Singleton;
 9  import javax.ejb.Startup;
10  import javax.ejb.TransactionManagement;
11  import javax.ejb.TransactionManagementType;
12  import javax.inject.Inject;
13  import javax.sql.DataSource;
14  import java.util.logging.Level;
15  import java.util.logging.Logger;
16  
17  /**
18   * Created by tqvarnst on 2017-04-04.
19   */
20  @Singleton
21  @Startup
22  @TransactionManagement(TransactionManagementType.BEAN)
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Producers.java
      * Line Number: 3
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Producers.java
      * Line Number: 4
      * Message: 'Replace the `javax.enterprise` import statement with `jakarta.enterprise`'
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
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/StartupListener.java
      * Line Number: 6
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
      * Code Snippet:
```java
 1  package com.redhat.coolstore.utils;
 2  
 3  import weblogic.application.ApplicationLifecycleEvent;
 4  import weblogic.application.ApplicationLifecycleListener;
 5  
 6  import javax.inject.Inject;
 7  import java.util.logging.Logger;
 8  
 9  public class StartupListener extends ApplicationLifecycleListener {
10  
11      @Inject
12      Logger log;
13  
14      @Override
15      public void postStart(ApplicationLifecycleEvent evt) {
16          log.info("AppListener(postStart)");
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 12
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 2  
 3  import com.redhat.coolstore.model.CatalogItemEntity;
 4  import com.redhat.coolstore.model.Order;
 5  import com.redhat.coolstore.model.OrderItem;
 6  import com.redhat.coolstore.model.Product;
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 13
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 3  import com.redhat.coolstore.model.CatalogItemEntity;
 4  import com.redhat.coolstore.model.Order;
 5  import com.redhat.coolstore.model.OrderItem;
 6  import com.redhat.coolstore.model.Product;
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
23   * Created by tqvarnst on 2017-03-30.
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 14
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 4  import com.redhat.coolstore.model.Order;
 5  import com.redhat.coolstore.model.OrderItem;
 6  import com.redhat.coolstore.model.Product;
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
23   * Created by tqvarnst on 2017-03-30.
24   */
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 15
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 5  import com.redhat.coolstore.model.OrderItem;
 6  import com.redhat.coolstore.model.Product;
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
23   * Created by tqvarnst on 2017-03-30.
24   */
25  public class Transformers {
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 16
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 6  import com.redhat.coolstore.model.Product;
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
23   * Created by tqvarnst on 2017-03-30.
24   */
25  public class Transformers {
26  
```
  * file:///opt/input/source/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 17
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
 7  import com.redhat.coolstore.model.ShoppingCart;
 8  import java.io.StringReader;
 9  import java.io.StringWriter;
10  import java.util.ArrayList;
11  import java.util.List;
12  import javax.json.Json;
13  import javax.json.JsonArray;
14  import javax.json.JsonArrayBuilder;
15  import javax.json.JsonObject;
16  import javax.json.JsonReader;
17  import javax.json.JsonWriter;
18  
19  import java.util.concurrent.ThreadLocalRandom;
20  import java.util.logging.Logger;
21  
22  /**
23   * Created by tqvarnst on 2017-03-30.
24   */
25  public class Transformers {
26  
27      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
```
### #10 - javax-to-jakarta-properties-00001
* Category: mandatory
* Effort: 1
* Description: Rename properties prefixed by javax with jakarta 
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///opt/input/source/src/main/resources/META-INF/persistence.xml
      * Line Number: 10
      * Message: 'Rename properties prefixed by `javax` with `jakarta`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
  * file:///opt/input/source/target/classes/META-INF/persistence.xml
      * Line Number: 10
      * Message: 'Rename properties prefixed by `javax` with `jakarta`'
      * Code Snippet:
```java
  1  <?xml version="1.0" encoding="UTF-8"?>
  2  <persistence version="2.1"
  3               xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  4               xsi:schemaLocation="
  5          http://xmlns.jcp.org/xml/ns/persistence
  6          http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  7      <persistence-unit name="primary">
  8          <jta-data-source>java:jboss/datasources/CoolstoreDS</jta-data-source>
  9          <properties>
 10              <property name="javax.persistence.schema-generation.database.action" value="none"/>
 11              <property name="hibernate.show_sql" value="false" />
 12              <property name="hibernate.format_sql" value="true" />
 13              <property name="hibernate.use_sql_comments" value="true" />
 14              <property name="hibernate.jdbc.use_get_generated_keys" value="false" />
 15          </properties>
 16      </persistence-unit>
 17  </persistence>

```
### #11 - javax-to-jakarta-servlet-00030
* Category: mandatory
* Effort: 3
* Description: The javax.servlet.http.HttpUtils utility class has been removed
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+, konveyor.io/target=jws, konveyor.io/target=jws6+
* Links
  * Red Hat JBoss EAP Application Migration from Jakarta EE 8 to EE 10 - Jakarta Servlet: https://access.redhat.com/articles/6980265#servlet
* Incidents
  * file:///root/.m2/repository/javax/javaee-web-api/7.0/javax/servlet/http/HttpUtils.java
      * Line Number: 74
      * Message: 'The `javax.servlet.http.HttpUtils` utility class has been removed. Applications should use the ServletRequest
 and HttpServletRequest interfaces instead of these methods it provided:
 - `parseQueryString(String s)` and `parsePostData(int len, ServletInputStream in)` -- Use `ServletRequest.getParameterMap()`. If an application needs to differentiate between query string parameters and request body parameters it will need to implement code to do that itself, perhaps by parsing the query string itself.
 - `getRequestURL(HttpServletRequest req)` -- Use `HttpServletRequest.getRequestURL()`.'
      * Code Snippet:
```java
64  import java.util.StringTokenizer;
65  import java.io.IOException;
66  
67  /**
68   * @deprecated		As of Java(tm) Servlet API 2.3. 
69   *			These methods were only useful
70   *			with the default encoding and have been moved
71   *			to the request interfaces.
72   *
73   */
74  public class HttpUtils {
75  
76      private static final String LSTRING_FILE =
77  	"javax.servlet.http.LocalStrings";
78      private static ResourceBundle lStrings =
79  	ResourceBundle.getBundle(LSTRING_FILE);
80          
81      
82      /**
83       * Constructs an empty <code>HttpUtils</code> object.
84       */
```
