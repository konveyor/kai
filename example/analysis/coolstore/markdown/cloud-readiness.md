# cloud-readiness
## Description
This ruleset detects logging configurations that may be problematic when migrating an application to a cloud environment.
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 1
### #0 - session-00000
* Category: mandatory
* Effort: 3
* Description: HTTP session replication (distributable web.xml)
* Labels: clustering, konveyor.io/source=java, konveyor.io/source=java-ee, konveyor.io/target=cloud-readiness
* Links
  * Getting Started with JBoss EAP for OpenShift Container Platform: Clustering: https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.3/html-single/getting_started_with_jboss_eap_for_openshift_container_platform/index#reference_clustering
  * JBoss EAP:  Externalize HTTP Sessions to Red Hat Data Grid: https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.3/html-single/configuration_guide/index#jdg_externalize_http_sessions
  * JBoss EAP: Clustering in Web Applications: https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.3/html/development_guide/clustering_in_web_applications
  * Running Data Grid on OpenShift: https://access.redhat.com/documentation/en-us/red_hat_data_grid/8.0/html-single/running_data_grid_on_openshift/index
  * Twelve-Factor App: Backing services: https://12factor.net/backing-services
  * Twelve-Factor App: Processes: https://12factor.net/processes
* Incidents
  * file:///tmp/source-code/src/main/webapp/WEB-INF/web.xml
      * Line Number: 5
      * Message: 'Session replication ensures that client sessions are not disrupted by node failure. Each node in the cluster shares information about ongoing sessions and can take over sessions if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.

 Recommendations

 * Review the session replication usage and ensure that it is configured properly.
 * Disable HTTP session clustering and accept its implications.
 * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.

 A remote data grid has the following benefits:

 * The application is more scaleable and elastic.
 * The application can survive EAP node failures because a JVM failure does not cause session data loss.
 * Session data can be shared by multiple applications.'
      * Code Snippet:
```java
  1  <!--suppress ServletWithoutMappingInspection -->
  2  <web-app xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  3           xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
  4           version="3.0">
  5      <distributable />
  6  </web-app>

```
