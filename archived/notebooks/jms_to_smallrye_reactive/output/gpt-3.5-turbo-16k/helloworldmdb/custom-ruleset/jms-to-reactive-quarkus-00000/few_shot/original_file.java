<?xml version="1.0" encoding="UTF-8"?>
<!--
    JBoss, Home of Professional Open Source
    Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
    contributors by the @authors tag. See the copyright.txt in the
    distribution for a full listing of individual contributors.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.jboss.eap.quickstarts</groupId>
    <version>7.4.0.GA</version>
    <artifactId>helloworld-mdb</artifactId>
    <packaging>war</packaging>
    <name>Quickstart: helloworld-mdb</name>
    <description>This project demonstrates a hello world Message-Driven Bean with Servlet 3.0 as client</description>

    <licenses>
        <license>
            <name>Apache License, Version 2.0</name>
            <url>http://www.apache.org/licenses/LICENSE-2.0.html</url>
            <distribution>repo</distribution>
        </license>
    </licenses>
<properties>

		<maven.compiler.source>1.8</maven.compiler.source>
		<maven.compiler.target>1.8</maven.compiler.target>

		<root.dir>${project.basedir}</root.dir>
		<jboss.home.name>EAP7_HOME</jboss.home.name>
		<product.name>JBoss EAP</product.name>
		<product.version>7.4.0.GA</product.version>
		<!-- A base list of dependency and plug-in version used in the various
		quick starts. -->
		<version.org.asciidoctor.asciidoctor-maven-plugin>2.1.0</version.org.asciidoctor.asciidoctor-maven-plugin>
		<version.wildfly.maven.plugin>2.0.2.Final</version.wildfly.maven.plugin>
		<version.org.wildfly.checkstyle-config>1.0.7.Final</version.org.wildfly.checkstyle-config>
		<version.org.wildfly.quickstarts.documentation.plugin>2.3.0.Final</version.org.wildfly.quickstarts.documentation.plugin>
		<!-- other plug-in versions -->
		<version.com.mycyla.license>3.0</version.com.mycyla.license>
		<version.checkstyle>8.5</version.checkstyle>
		<version.jaxws-tools-maven-plugin>1.2.3.Final</version.jaxws-tools-maven-plugin>
		<!-- Explicitly declaring the source encoding eliminates the following
		message: [WARNING] Using platform encoding (UTF-8 actually) to copy
		filtered resources, i.e. build is platform dependent! -->
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

		<!-- Protocol to use for communication with remote maven repositories.
		You can set to 'http' if you are using a maven proxy and 'https'
		interferes with that. Use 'https' for builds that will be released
                     to
		non-snapshot public maven repos -->
		<maven.repository.protocol>https</maven.repository.protocol>
		<!-- The full remote maven repo URL; can be overridden via -D for
		special use cases -->
		<maven.repository.url>
			${maven.repository.protocol}://repository.jboss.org/nexus/content/groups/public/</maven.repository.url>
		<!-- https://access.redhat.com/maven-repository -->
		<maven.redhat.repository.url>
			${maven.repository.protocol}://maven.repository.redhat.com/ga/</maven.redhat.repository.url>

		<!-- Version of BOMs
        note: a SNAPSHOT version *requires*
		checkout of BOMs at https://github.com/wildfly/boms and build through
		"mvn clean install"
        -->
		<version.server.bom>7.4.0.GA</version.server.bom>

		<!-- Versions of unmanaged dependencies -->
		<version.arquillian.angularjs.graphene>1.2.0.Beta1</version.arquillian.angularjs.graphene>
		<version.org.json>20150729</version.org.json>
		<version.ro.isdc.wro4j>1.7.9</version.ro.isdc.wro4j>

		<jboss.developer.drupal.url>http://rhdp-drupal.stage.redhat.com/</jboss.developer.drupal.url>
		<linkXRef>false</linkXRef>
		<version.microprofile.bom>3.0.0.GA</version.microprofile.bom>
		<version.war.plugin>3.3.2</version.war.plugin>
	</properties>
	<repositories>
		<repository>
			<releases>
				<enabled>true</enabled>
				<updatePolicy>never</updatePolicy>
			</releases>
			<snapshots>
				<enabled>true</enabled>
				<updatePolicy>never</updatePolicy>
			</snapshots>
			<id>jboss-public-repository-group</id>
			<name>JBoss Public Repository Group</name>
			<url>${maven.repository.url}</url>
			<layout>default</layout>
		</repository>
		<repository>
			<releases>
				<enabled>true</enabled>
				<updatePolicy>never</updatePolicy>
			</releases>
			<snapshots>
				<enabled>true</enabled>
				<updatePolicy>never</updatePolicy>
			</snapshots>
			<id>jboss-enterprise-maven-repository</id>
			<name>JBoss Enterprise Maven Repository</name>
			<url>${maven.redhat.repository.url}</url>
			<layout>default</layout>
		</repository>
	</repositories>
	<dependencyManagement>

		<dependencies>
			<!-- importing the jakartaee8-with-tools BOM adds specs and other
			useful artifacts as managed dependencies -->
			<dependency>
				<groupId>org.jboss.bom</groupId>
				<artifactId>jboss-eap-jakartaee8-with-tools</artifactId>
				<version>${version.server.bom}</version>
				<type>pom</type>
				<scope>import</scope>
			</dependency>
		</dependencies>
	</dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>jakarta.enterprise</groupId>
            <artifactId>jakarta.enterprise.cdi-api</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.jboss.spec.javax.ejb</groupId>
            <artifactId>jboss-ejb-api_3.2_spec</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.jboss.spec.javax.jms</groupId>
            <artifactId>jboss-jms-api_2.0_spec</artifactId>
            <scope>provided</scope>
        </dependency>
        <!-- Import the Servlet API, we use provided scope as the API is
            included in JBoss EAP -->
        <dependency>
            <groupId>org.jboss.spec.javax.servlet</groupId>
            <artifactId>jboss-servlet-api_4.0_spec</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.jboss.spec.javax.annotation</groupId>
            <artifactId>jboss-annotations-api_1.3_spec</artifactId>
            <scope>provided</scope>
        </dependency>

    </dependencies>
<build>
		<!-- Set the name of the WAR, used as the context root when the app is
		deployed -->
		<finalName>${project.artifactId}</finalName>
		<plugins>
			<plugin>
				<artifactId>maven-war-plugin</artifactId>
				<version>2.4</version>
				<configuration>
					<failOnMissingWebXml>false</failOnMissingWebXml>
				</configuration>
			</plugin>
			<plugin>
				<groupId>org.wildfly.plugins</groupId>
				<artifactId>wildfly-maven-plugin</artifactId>
				<version>${version.wildfly.maven.plugin}</version>
			</plugin>
		</plugins>
	</build>
	<profiles>
		<profile>
			<!-- When built in OpenShift the 'openshift' profile will be
                used
			when invoking mvn. -->
			<!-- Use this profile for any OpenShift specific customization
                your
			app will ne    ed. -->
			<!-- By default that is to put the resulting archive into the
			'deployments' folder. -->
			<!--
			http://maven.apache.org/guides/mini/guide-building-for-different-environments.html -->
			<id>openshift</id>
			<build>
				<plugins>
					<plugin>
						<groupId>org.apache.maven.plugins</groupId>
						<artifactId>maven-war-plugin</artifactId>
						<version>${version.war.plugin}</version>
						<configuration>
							<warName>ROOT</warName>
						</configuration>
					</plugin>
					<plugin>
						<groupId>org.apache.maven.plugins</groupId>
						<artifactId>maven-source-plugin</artifactId>
						<executions>
							<execution>
								<id>attach-sources</id>
								<phase>none</phase>
							</execution>
						</executions>
					</plugin>
				</plugins>
			</build>
		</profile>
	</profiles>
</project>
