# eap7/weblogic/tests/data
## Description

* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 1
### #0 - maven-javax-to-jakarta-00002
* Category: potential
* Effort: 1
* Description: Move to Jakarta EE Maven Artifacts - replace groupId javax.activation
* Labels: JakartaEE, konveyor.io/source, konveyor.io/target=eap, konveyor.io/target=eap7, konveyor.io/target=eap8, konveyor.io/target=jakarta-ee, konveyor.io/target=jakarta-ee8
* Links
  * Red Hat JBoss EAP 7.3 Migration Guide: Maven Artifact Changes for Jakarta EE: https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.3/html-single/migration_guide/index#maven-artifact-changes-for-jakarta-ee_default
* Incidents
  * file:///tmp/source-code/pom.xml
      * Message: 'If you migrate your application to JBoss EAP 7.3, or later, and want to ensure its Maven building, running or testing works as expected, use instead the Jakarta EE dependency with groupId `com.sun.activation`'
