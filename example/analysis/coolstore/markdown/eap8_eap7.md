# eap8/eap7
## Description
This ruleset provides analysis of Java EE applications that need to change certain CDI-related method calls.
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 10
### #0 - javaee-to-jakarta-namespaces-00001
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE namespace, schemaLocation and version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta EE XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#10
* Incidents
  * file:///tmp/source-code/src/main/webapp/WEB-INF/beans.xml
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
  * file:///tmp/source-code/src/main/webapp/WEB-INF/beans.xml
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
  * file:///tmp/source-code/src/main/webapp/WEB-INF/beans.xml
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
### #1 - javaee-to-jakarta-namespaces-00002
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE persistence namespace, schemaLocation and version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta Persistence XML Schemas: https://jakarta.ee/xml/ns/persistence/#3
* Incidents
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
### #2 - javaee-to-jakarta-namespaces-00006
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE XSD with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#9
* Incidents
  * file:///tmp/source-code/src/main/webapp/WEB-INF/beans.xml
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
### #3 - javaee-to-jakarta-namespaces-00030
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE XSD with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta XML Schemas: https://jakarta.ee/xml/ns/jakartaee/#9
* Incidents
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
### #4 - javaee-to-jakarta-namespaces-00033
* Category: mandatory
* Effort: 1
* Description: Replace the Java EE version with the Jakarta equivalent
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Incidents
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
### #5 - javax-to-jakarta-dependencies-00006
* Category: mandatory
* Effort: 1
* Description: javax groupId has been replaced by jakarta.platform
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///tmp/source-code/pom.xml
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
  * file:///tmp/source-code/pom.xml
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
### #6 - javax-to-jakarta-dependencies-00007
* Category: mandatory
* Effort: 1
* Description: javax javaee-api artifactId has been replaced by jakarta.platform jakarta.jakartaee-api
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #7 - javax-to-jakarta-dependencies-00008
* Category: mandatory
* Effort: 1
* Description: javax javaee-web-api artifactId has been replaced by jakarta.platform jakarta.jakartaee-web-api
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///tmp/source-code/pom.xml
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
### #8 - javax-to-jakarta-import-00001
* Category: mandatory
* Effort: 1
* Description: The package 'javax' has been replaced by 'jakarta'.
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 16  
 17  	private static final long serialVersionUID = 7526472295622776147L; 
 18  
 19      @Id
 20      private String itemId;
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 17  	private static final long serialVersionUID = 7526472295622776147L; 
 18  
 19      @Id
 20      private String itemId;
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 18  
 19      @Id
 20      private String itemId;
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 19      @Id
 20      private String itemId;
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 20      private String itemId;
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/InventoryEntity.java
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
 21  
 22  
 23      @Column
 24      private String location;
 25  
 26  
 27      @Column
 28      private int quantity;
 29  
 30  
 31      @Column
 32      private String link;
 33  
 34      public InventoryEntity() {
 35  
 36      }
 37  
 38      public String getItemId() {
 39  		return itemId;
 40  	}
 41  
 42  	public void setItemId(String itemId) {
 43  		this.itemId = itemId;
 44  	}
 45  
 46  	public String getLocation() {
 47  		return location;
 48  	}
 49  
 50  	public void setLocation(String location) {
 51  		this.location = location;
 52  	}
 53  
 54  	public int getQuantity() {
 55  		return quantity;
 56  	}
 57  
 58  	public void setQuantity(int quantity) {
 59  		this.quantity = quantity;
 60  	}
 61  
 62  	public String getLink() {
 63  		return link;
 64  	}
 65  
 66  	public void setLink(String link) {
 67  		this.link = link;
 68  	}
 69  
 70  	@Override
 71      public String toString() {
 72          return "InventoryEntity [itemId=" + itemId + ", availability=" + quantity + "/" + location + " link=" + link + "]";
 73      }
 74  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
111  		this.shippingDiscount = shippingDiscount;
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 12
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
111  		this.shippingDiscount = shippingDiscount;
112  	}
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 13
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
111  		this.shippingDiscount = shippingDiscount;
112  	}
113  
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 14
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
111  		this.shippingDiscount = shippingDiscount;
112  	}
113  
114  	public void setItemList(List<OrderItem> itemList) {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/Order.java
      * Line Number: 15
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
 35  	private double discount;
 36  
 37  	private double shippingFee;
 38  
 39  	private double shippingDiscount;
 40  
 41  	@Column(name="TOTAL_PRICE")
 42  
 43  	
 44  	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
 45  	@JoinColumn(name="ORDER_ID")
 46  	private List<OrderItem> itemList = new ArrayList<>();
 47  
 48  	public Order() {}
 49  
 50  	public long getOrderId() {
 51  		return orderId;
 52  	}
 53  
 54  	public void setOrderId(long orderId) {
 55  		this.orderId = orderId;
 56  	}
 57  
 58  	public String getCustomerName() {
 59  		return customerName;
 60  	}
 61  
 62  	public void setCustomerName(String customerName) {
 63  		this.customerName = customerName;
 64  	}
 65  
 66  	public String getCustomerEmail() {
 67  		return customerEmail;
 68  	}
 69  
 70  	public void setCustomerEmail(String customerEmail) {
 71  		this.customerEmail = customerEmail;
 72  	}
 73  
 74  	public double getOrderValue() {
 75  		return orderValue;
 76  	}
 77  
 78  	public void setOrderValue(double orderValue) {
 79  		this.orderValue = orderValue;
 80  	}
 81  
 82  	public double getRetailPrice() {
 83  		return retailPrice;
 84  	}
 85  
 86  	public void setRetailPrice(double retailPrice) {
 87  		this.retailPrice = retailPrice;
 88  	}
 89  
 90  	public double getDiscount() {
 91  		return discount;
 92  	}
 93  
 94  	public void setDiscount(double discount) {
 95  		this.discount = discount;
 96  	}
 97  
 98  	public double getShippingFee() {
 99  		return shippingFee;
100  	}
101  
102  	public void setShippingFee(double shippingFee) {
103  		this.shippingFee = shippingFee;
104  	}
105  
106  	public double getShippingDiscount() {
107  		return shippingDiscount;
108  	}
109  
110  	public void setShippingDiscount(double shippingDiscount) {
111  		this.shippingDiscount = shippingDiscount;
112  	}
113  
114  	public void setItemList(List<OrderItem> itemList) {
115  		this.itemList = itemList;
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/OrderItem.java
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
 29  	}
 30  
 31  	public void setProductId(String productId) {
 32  		this.productId = productId;
 33  	}
 34  
 35  	public int getQuantity() {
 36  		return quantity;
 37  	}
 38  
 39  	public void setQuantity(int quantity) {
 40  		this.quantity = quantity;
 41  	}
 42  
 43  	@Override
 44  	public String toString() {
 45  		return "OrderItem [productId=" + productId + ", quantity=" + quantity + "]";
 46  	}
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/OrderItem.java
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
 29  	}
 30  
 31  	public void setProductId(String productId) {
 32  		this.productId = productId;
 33  	}
 34  
 35  	public int getQuantity() {
 36  		return quantity;
 37  	}
 38  
 39  	public void setQuantity(int quantity) {
 40  		this.quantity = quantity;
 41  	}
 42  
 43  	@Override
 44  	public String toString() {
 45  		return "OrderItem [productId=" + productId + ", quantity=" + quantity + "]";
 46  	}
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/OrderItem.java
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
 29  	}
 30  
 31  	public void setProductId(String productId) {
 32  		this.productId = productId;
 33  	}
 34  
 35  	public int getQuantity() {
 36  		return quantity;
 37  	}
 38  
 39  	public void setQuantity(int quantity) {
 40  		this.quantity = quantity;
 41  	}
 42  
 43  	@Override
 44  	public String toString() {
 45  		return "OrderItem [productId=" + productId + ", quantity=" + quantity + "]";
 46  	}
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/OrderItem.java
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
 29  	}
 30  
 31  	public void setProductId(String productId) {
 32  		this.productId = productId;
 33  	}
 34  
 35  	public int getQuantity() {
 36  		return quantity;
 37  	}
 38  
 39  	public void setQuantity(int quantity) {
 40  		this.quantity = quantity;
 41  	}
 42  
 43  	@Override
 44  	public String toString() {
 45  		return "OrderItem [productId=" + productId + ", quantity=" + quantity + "]";
 46  	}
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/OrderItem.java
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
 20  
 21  	private int quantity;
 22  
 23  	private String productId;
 24  
 25  	public OrderItem() {}
 26  
 27  	public String getProductId() {
 28  		return productId;
 29  	}
 30  
 31  	public void setProductId(String productId) {
 32  		this.productId = productId;
 33  	}
 34  
 35  	public int getQuantity() {
 36  		return quantity;
 37  	}
 38  
 39  	public void setQuantity(int quantity) {
 40  		this.quantity = quantity;
 41  	}
 42  
 43  	@Override
 44  	public String toString() {
 45  		return "OrderItem [productId=" + productId + ", quantity=" + quantity + "]";
 46  	}
 47  
 48  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/model/ShoppingCart.java
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
 18  	private double shippingTotal;
 19  	
 20  	private double shippingPromoSavings;
 21  	
 22  	private double cartTotal;
 23  			
 24  	private List<ShoppingCartItem> shoppingCartItemList = new ArrayList<ShoppingCartItem>();
 25  
 26  	public ShoppingCart() {
 27  		
 28  	}
 29  	
 30  	public List<ShoppingCartItem> getShoppingCartItemList() {
 31  		return shoppingCartItemList;
 32  	}
 33  
 34  	public void setShoppingCartItemList(List<ShoppingCartItem> shoppingCartItemList) {
 35  		this.shoppingCartItemList = shoppingCartItemList;
 36  	}
 37  
 38  	public void resetShoppingCartItemList() {
 39  		shoppingCartItemList = new ArrayList<ShoppingCartItem>();
 40  	}
 41  
 42  	public void addShoppingCartItem(ShoppingCartItem sci) {
 43  		
 44  		if ( sci != null ) {
 45  			
 46  			shoppingCartItemList.add(sci);
 47  			
 48  		}
 49  		
 50  	}
 51  	
 52  	public boolean removeShoppingCartItem(ShoppingCartItem sci) {
 53  		
 54  		boolean removed = false;
 55  		
 56  		if ( sci != null ) {
 57  			
 58  			removed = shoppingCartItemList.remove(sci);
 59  			
 60  		}
 61  		
 62  		return removed;
 63  		
 64  	}
 65  
 66  	public double getCartItemTotal() {
 67  		return cartItemTotal;
 68  	}
 69  
 70  	public void setCartItemTotal(double cartItemTotal) {
 71  		this.cartItemTotal = cartItemTotal;
 72  	}
 73  
 74  	public double getShippingTotal() {
 75  		return shippingTotal;
 76  	}
 77  
 78  	public void setShippingTotal(double shippingTotal) {
 79  		this.shippingTotal = shippingTotal;
 80  	}
 81  
 82  	public double getCartTotal() {
 83  		return cartTotal;
 84  	}
 85  
 86  	public void setCartTotal(double cartTotal) {
 87  		this.cartTotal = cartTotal;
 88  	}
 89  
 90  	public double getCartItemPromoSavings() {
 91  		return cartItemPromoSavings;
 92  	}
 93  
 94  	public void setCartItemPromoSavings(double cartItemPromoSavings) {
 95  		this.cartItemPromoSavings = cartItemPromoSavings;
 96  	}
 97  
 98  	public double getShippingPromoSavings() {
 99  		return shippingPromoSavings;
100  	}
101  
102  	public void setShippingPromoSavings(double shippingPromoSavings) {
103  		this.shippingPromoSavings = shippingPromoSavings;
104  	}
105  
106  	@Override
107  	public String toString() {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
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
 14      @Produces
 15      public EntityManager getEntityManager() {
 16          return em;
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
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
 15      public EntityManager getEntityManager() {
 16          return em;
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
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
 16          return em;
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
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
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
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
 20  import com.redhat.coolstore.model.ShoppingCart;
 21  import com.redhat.coolstore.model.ShoppingCartItem;
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
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
 21  import com.redhat.coolstore.model.ShoppingCartItem;
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 12
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 13
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
113  						toRemoveList.add(sci);
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 14
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
113  						toRemoveList.add(sci);
114  					} else {
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 15
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
113  						toRemoveList.add(sci);
114  					} else {
115  						sci.setQuantity(sci.getQuantity() - quantity);
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 16
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
113  						toRemoveList.add(sci);
114  					} else {
115  						sci.setQuantity(sci.getQuantity() - quantity);
116  					}
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/CartEndpoint.java
      * Line Number: 17
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
 22  import com.redhat.coolstore.service.ShoppingCartService;
 23  
 24  @SessionScoped
 25  @Path("/cart")
 26  public class CartEndpoint implements Serializable {
 27  
 28  	private static final long serialVersionUID = -7227732980791688773L;
 29  
 30  	@Inject
 31  	private ShoppingCartService shoppingCartService;
 32  
 33  	@GET
 34  	@Path("/{cartId}")
 35  	@Produces(MediaType.APPLICATION_JSON)
 36  	public ShoppingCart getCart(@PathParam("cartId") String cartId) {
 37  		return shoppingCartService.getShoppingCart(cartId);
 38  	}
 39  
 40  	@POST
 41  	@Path("/checkout/{cartId}")
 42  	@Produces(MediaType.APPLICATION_JSON)
 43  	public ShoppingCart checkout(@PathParam("cartId") String cartId) {
 44  		return shoppingCartService.checkOutShoppingCart(cartId);
 45  	}
 46  
 47  	@POST
 48  	@Path("/{cartId}/{itemId}/{quantity}")
 49  	@Produces(MediaType.APPLICATION_JSON)
 50  	public ShoppingCart add(@PathParam("cartId") String cartId,
 51  							@PathParam("itemId") String itemId,
 52  							@PathParam("quantity") int quantity) throws Exception {
 53  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 54  
 55  		Product product = shoppingCartService.getProduct(itemId);
 56  
 57  		ShoppingCartItem sci = new ShoppingCartItem();
 58  		sci.setProduct(product);
 59  		sci.setQuantity(quantity);
 60  		sci.setPrice(product.getPrice());
 61  		cart.addShoppingCartItem(sci);
 62  
 63  		try {
 64  			shoppingCartService.priceShoppingCart(cart);
 65  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 66  		} catch (Exception ex) {
 67  			cart.removeShoppingCartItem(sci);
 68  			throw ex;
 69  		}
 70  
 71  		return cart;
 72  	}
 73  
 74  	@POST
 75  	@Path("/{cartId}/{tmpId}")
 76  	@Produces(MediaType.APPLICATION_JSON)
 77  	public ShoppingCart set(@PathParam("cartId") String cartId,
 78  							@PathParam("tmpId") String tmpId) throws Exception {
 79  
 80  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
 81  		ShoppingCart tmpCart = shoppingCartService.getShoppingCart(tmpId);
 82  
 83  		if (tmpCart != null) {
 84  			cart.resetShoppingCartItemList();
 85  			cart.setShoppingCartItemList(tmpCart.getShoppingCartItemList());
 86  		}
 87  
 88  		try {
 89  			shoppingCartService.priceShoppingCart(cart);
 90  			cart.setShoppingCartItemList(dedupeCartItems(cart.getShoppingCartItemList()));
 91  		} catch (Exception ex) {
 92  			throw ex;
 93  		}
 94  
 95  		return cart;
 96  	}
 97  
 98  	@DELETE
 99  	@Path("/{cartId}/{itemId}/{quantity}")
100  	@Produces(MediaType.APPLICATION_JSON)
101  	public ShoppingCart delete(@PathParam("cartId") String cartId,
102  							   @PathParam("itemId") String itemId,
103  							   @PathParam("quantity") int quantity) throws Exception {
104  
105  		List<ShoppingCartItem> toRemoveList = new ArrayList<>();
106  
107  		ShoppingCart cart = shoppingCartService.getShoppingCart(cartId);
108  
109  		cart.getShoppingCartItemList().stream()
110  				.filter(sci -> sci.getProduct().getItemId().equals(itemId))
111  				.forEach(sci -> {
112  					if (quantity >= sci.getQuantity()) {
113  						toRemoveList.add(sci);
114  					} else {
115  						sci.setQuantity(sci.getQuantity() - quantity);
116  					}
117  				});
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 17  
 18  @RequestScoped
 19  @Path("/orders")
 20  @Consumes(MediaType.APPLICATION_JSON)
 21  @Produces(MediaType.APPLICATION_JSON)
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 18  @RequestScoped
 19  @Path("/orders")
 20  @Consumes(MediaType.APPLICATION_JSON)
 21  @Produces(MediaType.APPLICATION_JSON)
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 19  @Path("/orders")
 20  @Consumes(MediaType.APPLICATION_JSON)
 21  @Produces(MediaType.APPLICATION_JSON)
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 20  @Consumes(MediaType.APPLICATION_JSON)
 21  @Produces(MediaType.APPLICATION_JSON)
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 21  @Produces(MediaType.APPLICATION_JSON)
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
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
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 12
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
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/OrderEndpoint.java
      * Line Number: 13
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
 22  public class OrderEndpoint implements Serializable {
 23  
 24      private static final long serialVersionUID = -7227732980791688774L;
 25  
 26      @Inject
 27      private OrderService os;
 28  
 29  
 30      @GET
 31      @Path("/")
 32      public List<Order> listAll() {
 33          return os.getOrders();
 34      }
 35  
 36      @GET
 37      @Path("/{orderId}")
 38      public Order getOrder(@PathParam("orderId") long orderId) {
 39          return os.getOrderById(orderId);
 40      }
 41  
 42  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
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
 17  @Produces(MediaType.APPLICATION_JSON)
 18  public class ProductEndpoint implements Serializable {
 19  
 20      /**
 21       *
 22       */
 23      private static final long serialVersionUID = -7227732980791688773L;
 24  
 25      @Inject
 26      private ProductService pm;
 27  
 28  
 29      @GET
 30      @Path("/")
 31      public List<Product> listAll() {
 32          return pm.getProducts();
 33      }
 34  
 35      @GET
 36      @Path("/{itemId}")
 37      public Product getProduct(@PathParam("itemId") String itemId) {
 38          return pm.getProductByItemId(itemId);
 39      }
 40  
 41  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
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
 18  public class ProductEndpoint implements Serializable {
 19  
 20      /**
 21       *
 22       */
 23      private static final long serialVersionUID = -7227732980791688773L;
 24  
 25      @Inject
 26      private ProductService pm;
 27  
 28  
 29      @GET
 30      @Path("/")
 31      public List<Product> listAll() {
 32          return pm.getProducts();
 33      }
 34  
 35      @GET
 36      @Path("/{itemId}")
 37      public Product getProduct(@PathParam("itemId") String itemId) {
 38          return pm.getProductByItemId(itemId);
 39      }
 40  
 41  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/ProductEndpoint.java
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
 20      /**
 21       *
 22       */
 23      private static final long serialVersionUID = -7227732980791688773L;
 24  
 25      @Inject
 26      private ProductService pm;
 27  
 28  
 29      @GET
 30      @Path("/")
 31      public List<Product> listAll() {
 32          return pm.getProducts();
 33      }
 34  
 35      @GET
 36      @Path("/{itemId}")
 37      public Product getProduct(@PathParam("itemId") String itemId) {
 38          return pm.getProductByItemId(itemId);
 39      }
 40  
 41  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/RestApplication.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/rest/RestApplication.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 12
      * Message: 'Replace the `javax.ejb` import statement with `jakarta.ejb`'
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 13
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java
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
 17  
 18      @Inject
 19      private CatalogService catalogService;
 20  
 21      private final static String JNDI_FACTORY = "weblogic.jndi.WLInitialContextFactory";
 22      private final static String JMS_FACTORY = "TCF";
 23      private final static String TOPIC = "topic/orders";
 24      private TopicConnection tcon;
 25      private TopicSession tsession;
 26      private TopicSubscriber tsubscriber;
 27  
 28      public void onMessage(Message rcvMessage) {
 29          TextMessage msg;
 30          {
 31              try {
 32                  System.out.println("received message inventory");
 33                  if (rcvMessage instanceof TextMessage) {
 34                      msg = (TextMessage) rcvMessage;
 35                      String orderStr = msg.getBody(String.class);
 36                      Order order = Transformers.jsonToOrder(orderStr);
 37                      order.getItemList().forEach(orderItem -> {
 38                          int old_quantity = catalogService.getCatalogItemById(orderItem.getProductId()).getInventory().getQuantity();
 39                          int new_quantity = old_quantity - orderItem.getQuantity();
 40                          if (new_quantity < LOW_THRESHOLD) {
 41                              System.out.println("Inventory for item " + orderItem.getProductId() + " is below threshold (" + LOW_THRESHOLD + "), contact supplier!");
 42                          } else {
 43                              orderItem.setQuantity(new_quantity);
 44                          }
 45                      });
 46                  }
 47  
 48  
 49              } catch (JMSException jmse) {
 50                  System.err.println("An exception occurred: " + jmse.getMessage());
 51              }
 52          }
 53      }
 54  
 55      public void init() throws NamingException, JMSException {
 56          Context ctx = getInitialContext();
 57          TopicConnectionFactory tconFactory = (TopicConnectionFactory) PortableRemoteObject.narrow(ctx.lookup(JMS_FACTORY), TopicConnectionFactory.class);
 58          tcon = tconFactory.createTopicConnection();
 59          tsession = tcon.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);
 60          Topic topic = (Topic) PortableRemoteObject.narrow(ctx.lookup(TOPIC), Topic.class);
 61          tsubscriber = tsession.createSubscriber(topic);
 62          tsubscriber.setMessageListener(this);
 63          tcon.start();
 64      }
 65  
 66      public void close() throws JMSException {
 67          tsubscriber.close();
 68          tsession.close();
 69          tcon.close();
 70      }
 71  
 72      private static InitialContext getInitialContext() throws NamingException {
 73          Hashtable<String, String> env = new Hashtable<>();
 74          env.put(Context.INITIAL_CONTEXT_FACTORY, JNDI_FACTORY);
 75          env.put(Context.PROVIDER_URL, "t3://localhost:7001");
 76          env.put("weblogic.jndi.createIntermediateContexts", "true");
 77          return new InitialContext(env);
 78      }
 79  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 19  
 20  	@Inject
 21  	OrderService orderService;
 22  
 23  	@Inject
 24  	CatalogService catalogService;
 25  
 26  	@Override
 27  	public void onMessage(Message rcvMessage) {
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
 20  	@Inject
 21  	OrderService orderService;
 22  
 23  	@Inject
 24  	CatalogService catalogService;
 25  
 26  	@Override
 27  	public void onMessage(Message rcvMessage) {
 28  		System.out.println("\nMessage recd !");
 29  		TextMessage msg = null;
 30  		try {
 31  				if (rcvMessage instanceof TextMessage) {
 32  						msg = (TextMessage) rcvMessage;
 33  						String orderStr = msg.getBody(String.class);
 34  						System.out.println("Received order: " + orderStr);
 35  						Order order = Transformers.jsonToOrder(orderStr);
 36  						System.out.println("Order object is " + order);
 37  						orderService.save(order);
 38  						order.getItemList().forEach(orderItem -> {
 39  							catalogService.updateInventoryItems(orderItem.getProductId(), orderItem.getQuantity());
 40  						});
 41  				}
 42  		} catch (JMSException e) {
 43  			throw new RuntimeException(e);
 44  		}
 45  	}
 46  
 47  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ProductService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ProductService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/PromoService.java
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
 20      private String name = null;
 21  
 22      private Set<Promotion> promotionSet = null;
 23  
 24      public PromoService() {
 25  
 26          promotionSet = new HashSet<>();
 27  
 28          promotionSet.add(new Promotion("329299", .25));
 29  
 30      }
 31  
 32      public void applyCartItemPromotions(ShoppingCart shoppingCart) {
 33  
 34          if (shoppingCart != null && shoppingCart.getShoppingCartItemList().size() > 0) {
 35  
 36              Map<String, Promotion> promoMap = new HashMap<String, Promotion>();
 37  
 38              for (Promotion promo : getPromotions()) {
 39  
 40                  promoMap.put(promo.getItemId(), promo);
 41  
 42              }
 43  
 44              for (ShoppingCartItem sci : shoppingCart.getShoppingCartItemList()) {
 45  
 46                  String productId = sci.getProduct().getItemId();
 47  
 48                  Promotion promo = promoMap.get(productId);
 49  
 50                  if (promo != null) {
 51  
 52                      sci.setPromoSavings(sci.getProduct().getPrice() * promo.getPercentOff() * -1);
 53                      sci.setPrice(sci.getProduct().getPrice() * (1 - promo.getPercentOff()));
 54  
 55                  }
 56  
 57              }
 58  
 59          }
 60  
 61      }
 62  
 63      public void applyShippingPromotions(ShoppingCart shoppingCart) {
 64  
 65          if (shoppingCart != null) {
 66  
 67              //PROMO: if cart total is greater than 75, free shipping
 68              if (shoppingCart.getCartItemTotal() >= 75) {
 69  
 70                  shoppingCart.setShippingPromoSavings(shoppingCart.getShippingTotal() * -1);
 71                  shoppingCart.setShippingTotal(0);
 72  
 73              }
 74  
 75          }
 76  
 77      }
 78  
 79      public Set<Promotion> getPromotions() {
 80  
 81          if (promotionSet == null) {
 82  
 83              promotionSet = new HashSet<>();
 84  
 85          }
 86  
 87          return new HashSet<>(promotionSet);
 88  
 89      }
 90  
 91      public void setPromotions(Set<Promotion> promotionSet) {
 92  
 93          if (promotionSet != null) {
 94  
 95              this.promotionSet = new HashSet<>(promotionSet);
 96  
 97          } else {
 98  
 99              this.promotionSet = new HashSet<>();
100  
101          }
102  
103      }
104  
105      @Override
106      public String toString() {
107          return "PromoService [name=" + name + ", promotionSet=" + promotionSet + "]";
108      }
109  
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartService.java
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
 27  
 28  
 29      @Inject
 30      ShoppingCartOrderProcessor shoppingCartOrderProcessor;
 31  
 32      private ShoppingCart cart  = new ShoppingCart(); //Each user can have multiple shopping carts (tabbed browsing)
 33  
 34     
 35  
 36      public ShoppingCartService() {
 37      }
 38  
 39      public ShoppingCart getShoppingCart(String cartId) {
 40          return cart;
 41      }
 42  
 43      public ShoppingCart checkOutShoppingCart(String cartId) {
 44          ShoppingCart cart = this.getShoppingCart(cartId);
 45        
 46          log.info("Sending  order: ");
 47          shoppingCartOrderProcessor.process(cart);
 48     
 49          cart.resetShoppingCartItemList();
 50          priceShoppingCart(cart);
 51          return cart;
 52      }
 53  
 54      public void priceShoppingCart(ShoppingCart sc) {
 55  
 56          if (sc != null) {
 57  
 58              initShoppingCartForPricing(sc);
 59  
 60              if (sc.getShoppingCartItemList() != null && sc.getShoppingCartItemList().size() > 0) {
 61  
 62                  ps.applyCartItemPromotions(sc);
 63  
 64                  for (ShoppingCartItem sci : sc.getShoppingCartItemList()) {
 65  
 66                      sc.setCartItemPromoSavings(
 67                              sc.getCartItemPromoSavings() + sci.getPromoSavings() * sci.getQuantity());
 68                      sc.setCartItemTotal(sc.getCartItemTotal() + sci.getPrice() * sci.getQuantity());
 69  
 70                  }
 71  
 72                  sc.setShippingTotal(lookupShippingServiceRemote().calculateShipping(sc));
 73  
 74                  if (sc.getCartItemTotal() >= 25) {
 75                      sc.setShippingTotal(sc.getShippingTotal()
 76                              + lookupShippingServiceRemote().calculateShippingInsurance(sc));
 77                  }
 78  
 79              }
 80  
 81              ps.applyShippingPromotions(sc);
 82  
 83              sc.setCartTotal(sc.getCartItemTotal() + sc.getShippingTotal());
 84  
 85          }
 86  
 87      }
 88  
 89      private void initShoppingCartForPricing(ShoppingCart sc) {
 90  
 91          sc.setCartItemTotal(0);
 92          sc.setCartItemPromoSavings(0);
 93          sc.setShippingTotal(0);
 94          sc.setShippingPromoSavings(0);
 95          sc.setCartTotal(0);
 96  
 97          for (ShoppingCartItem sci : sc.getShoppingCartItemList()) {
 98              Product p = getProduct(sci.getProduct().getItemId());
 99              //if product exist
100              if (p != null) {
101                  sci.setProduct(p);
102                  sci.setPrice(p.getPrice());
103              }
104  
105              sci.setPromoSavings(0);
106          }
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartService.java
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
 18  
 19      @Inject
 20      Logger log;
 21  
 22      @Inject
 23      ProductService productServices;
 24  
 25      @Inject
 26      PromoService ps;
 27  
 28  
 29      @Inject
 30      ShoppingCartOrderProcessor shoppingCartOrderProcessor;
 31  
 32      private ShoppingCart cart  = new ShoppingCart(); //Each user can have multiple shopping carts (tabbed browsing)
 33  
 34     
 35  
 36      public ShoppingCartService() {
 37      }
 38  
 39      public ShoppingCart getShoppingCart(String cartId) {
 40          return cart;
 41      }
 42  
 43      public ShoppingCart checkOutShoppingCart(String cartId) {
 44          ShoppingCart cart = this.getShoppingCart(cartId);
 45        
 46          log.info("Sending  order: ");
 47          shoppingCartOrderProcessor.process(cart);
 48     
 49          cart.resetShoppingCartItemList();
 50          priceShoppingCart(cart);
 51          return cart;
 52      }
 53  
 54      public void priceShoppingCart(ShoppingCart sc) {
 55  
 56          if (sc != null) {
 57  
 58              initShoppingCartForPricing(sc);
 59  
 60              if (sc.getShoppingCartItemList() != null && sc.getShoppingCartItemList().size() > 0) {
 61  
 62                  ps.applyCartItemPromotions(sc);
 63  
 64                  for (ShoppingCartItem sci : sc.getShoppingCartItemList()) {
 65  
 66                      sc.setCartItemPromoSavings(
 67                              sc.getCartItemPromoSavings() + sci.getPromoSavings() * sci.getQuantity());
 68                      sc.setCartItemTotal(sc.getCartItemTotal() + sci.getPrice() * sci.getQuantity());
 69  
 70                  }
 71  
 72                  sc.setShippingTotal(lookupShippingServiceRemote().calculateShipping(sc));
 73  
 74                  if (sc.getCartItemTotal() >= 25) {
 75                      sc.setShippingTotal(sc.getShippingTotal()
 76                              + lookupShippingServiceRemote().calculateShippingInsurance(sc));
 77                  }
 78  
 79              }
 80  
 81              ps.applyShippingPromotions(sc);
 82  
 83              sc.setCartTotal(sc.getCartItemTotal() + sc.getShippingTotal());
 84  
 85          }
 86  
 87      }
 88  
 89      private void initShoppingCartForPricing(ShoppingCart sc) {
 90  
 91          sc.setCartItemTotal(0);
 92          sc.setCartItemPromoSavings(0);
 93          sc.setShippingTotal(0);
 94          sc.setShippingPromoSavings(0);
 95          sc.setCartTotal(0);
 96  
 97          for (ShoppingCartItem sci : sc.getShoppingCartItemList()) {
 98              Product p = getProduct(sci.getProduct().getItemId());
 99              //if product exist
100              if (p != null) {
101                  sci.setProduct(p);
102                  sci.setPrice(p.getPrice());
103              }
104  
105              sci.setPromoSavings(0);
106          }
107  
```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 17  /**
 18   * Created by tqvarnst on 2017-04-04.
 19   */
 20  @Singleton
 21  @Startup
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 18   * Created by tqvarnst on 2017-04-04.
 19   */
 20  @Singleton
 21  @Startup
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 19   */
 20  @Singleton
 21  @Startup
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 20  @Singleton
 21  @Startup
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 21  @Startup
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
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
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/DataBaseMigrationStartup.java
      * Line Number: 12
      * Message: 'Replace the `javax.inject` import statement with `jakarta.inject`'
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
 22  @TransactionManagement(TransactionManagementType.BEAN)
 23  public class DataBaseMigrationStartup {
 24  
 25      @Inject
 26      Logger logger;
 27  
 28      @Resource(mappedName = "java:jboss/datasources/CoolstoreDS")
 29      DataSource dataSource;
 30  
 31      @PostConstruct
 32      private void startup() {
 33  
 34  
 35          try {
 36              logger.info("Initializing/migrating the database using FlyWay");
 37              Flyway flyway = new Flyway();
 38              flyway.setDataSource(dataSource);
 39              flyway.baseline();
 40              // Start the db.migration
 41              flyway.migrate();
 42          } catch (FlywayException e) {
 43              if(logger !=null)
 44                  logger.log(Level.SEVERE,"FAILED TO INITIALIZE THE DATABASE: " + e.getMessage(),e);
 45              else
 46                  System.out.println("FAILED TO INITIALIZE THE DATABASE: " + e.getMessage() + " and injection of logger doesn't work");
 47  
 48          }
 49      }
 50  
 51  
 52  
 53  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Producers.java
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
 14          return Logger.getLogger(injectionPoint.getMember().getDeclaringClass().getName());
 15      }
 16  
 17  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Producers.java
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
 15      }
 16  
 17  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/StartupListener.java
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
 17      }
 18  
 19      @Override
 20      public void preStop(ApplicationLifecycleEvent evt) {
 21          log.info("AppListener(preStop)");
 22      }
 23  
 24  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 13
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 14
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 15
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 16
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 17
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/utils/Transformers.java
      * Line Number: 18
      * Message: 'Replace the `javax.json` import statement with `jakarta.json`'
      * Code Snippet:
```java
  1  package com.redhat.coolstore.utils;
  2  
  3  import com.redhat.coolstore.model.CatalogItemEntity;
  4  import com.redhat.coolstore.model.Order;
  5  import com.redhat.coolstore.model.OrderItem;
  6  import com.redhat.coolstore.model.Product;
  7  import com.redhat.coolstore.model.ProductImpl;
  8  import com.redhat.coolstore.model.ShoppingCart;
  9  import java.io.StringReader;
 10  import java.io.StringWriter;
 11  import java.util.ArrayList;
 12  import java.util.List;
 13  import javax.json.Json;
 14  import javax.json.JsonArray;
 15  import javax.json.JsonArrayBuilder;
 16  import javax.json.JsonObject;
 17  import javax.json.JsonReader;
 18  import javax.json.JsonWriter;
 19  
 20  import java.util.concurrent.ThreadLocalRandom;
 21  import java.util.logging.Logger;
 22  
 23  /**
 24   * Created by tqvarnst on 2017-03-30.
 25   */
 26  public class Transformers {
 27  
 28      private static final String[] RANDOM_NAMES = {"Sven Karlsson","Johan Andersson","Karl Svensson","Anders Johansson","Stefan Olson","Martin Ericsson"};
 29      private static final String[] RANDOM_EMAILS = {"sven@gmail.com","johan@gmail.com","karl@gmail.com","anders@gmail.com","stefan@gmail.com","martin@gmail.com"};
 30  
 31      private static Logger log = Logger.getLogger(Transformers.class.getName());
 32  
 33      public static Product toProduct(CatalogItemEntity entity) {
 34          ProductImpl prod = new ProductImpl();
 35          prod.setItemId(entity.getItemId());
 36          prod.setName(entity.getName());
 37          prod.setDesc(entity.getDesc());
 38          prod.setPrice(entity.getPrice());
 39          if (entity.getInventory() != null) {
 40              prod.setLocation(entity.getInventory().getLocation());
 41              prod.setLink(entity.getInventory().getLink());
 42              prod.setQuantity(entity.getInventory().getQuantity());
 43          } else {
 44              log.warning("Inventory for " + entity.getName() + "[" + entity.getItemId()+ "] unknown and missing");
 45          }
 46          return prod;
 47      }
 48  
 49      public static String shoppingCartToJson(ShoppingCart cart) {
 50          JsonArrayBuilder cartItems = Json.createArrayBuilder();
 51          cart.getShoppingCartItemList().forEach(item -> {
 52              cartItems.add(Json.createObjectBuilder()
 53                  .add("productSku",item.getProduct().getItemId())
 54                  .add("quantity",item.getQuantity())
 55              );
 56          });
 57  
 58          int randomNameAndEmailIndex = ThreadLocalRandom.current().nextInt(RANDOM_NAMES.length);
 59  
 60          JsonObject jsonObject = Json.createObjectBuilder()
 61              .add("orderValue", Double.valueOf(cart.getCartTotal()))
 62              .add("customerName",RANDOM_NAMES[randomNameAndEmailIndex])
 63              .add("customerEmail",RANDOM_EMAILS[randomNameAndEmailIndex])
 64              .add("retailPrice", cart.getShoppingCartItemList().stream().mapToDouble(i -> i.getQuantity()*i.getPrice()).sum())
 65              .add("discount", Double.valueOf(cart.getCartItemPromoSavings()))
 66              .add("shippingFee", Double.valueOf(cart.getShippingTotal()))
 67              .add("shippingDiscount", Double.valueOf(cart.getShippingPromoSavings()))
 68              .add("items",cartItems) 
 69              .build();
 70          StringWriter w = new StringWriter();
 71          try (JsonWriter writer = Json.createWriter(w)) {
 72              writer.write(jsonObject);
 73          }
 74          return w.toString();
 75      }
 76  
 77      public static Order jsonToOrder(String json) {
 78          JsonReader jsonReader = Json.createReader(new StringReader(json));
 79          JsonObject rootObject = jsonReader.readObject();
 80          Order order = new Order();
 81          order.setCustomerName(rootObject.getString("customerName"));
 82          order.setCustomerEmail(rootObject.getString("customerEmail"));
 83          order.setOrderValue(rootObject.getJsonNumber("orderValue").doubleValue());
 84          order.setRetailPrice(rootObject.getJsonNumber("retailPrice").doubleValue());
 85          order.setDiscount(rootObject.getJsonNumber("discount").doubleValue());
 86          order.setShippingFee(rootObject.getJsonNumber("shippingFee").doubleValue());
 87          order.setShippingDiscount(rootObject.getJsonNumber("shippingDiscount").doubleValue());
 88          JsonArray jsonItems = rootObject.getJsonArray("items");
 89          List<OrderItem> items = new ArrayList<OrderItem>(jsonItems.size());
 90          for (JsonObject jsonItem : jsonItems.getValuesAs(JsonObject.class)) {
 91              OrderItem oi = new OrderItem();
 92              oi.setProductId(jsonItem.getString("productSku"));
 93              oi.setQuantity(jsonItem.getInt("quantity"));
 94              items.add(oi);
 95          }
 96          order.setItemList(items); 
 97          return order;
 98      }
 99  
100  
101  }

```
### #9 - javax-to-jakarta-properties-00001
* Category: mandatory
* Effort: 1
* Description: Rename properties prefixed by javax with jakarta 
* Labels: konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee9+
* Links
  * Jakarta EE: https://jakarta.ee/
* Incidents
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
