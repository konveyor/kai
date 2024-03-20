# kai/quarkus
## Description
Quarkus focused rules to help migrate from Java EE
* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated
## Violations
Number of Violations: 8
### #0 - jms-to-reactive-quarkus-00000
* Category: mandatory
* Effort: 5
* Description: JMS is not supported in Quarkus
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides
  * Smallrye Reactive - Connectors: https://smallrye.io/smallrye-reactive-messaging/smallrye-reactive-messaging/3.4/connectors/connectors.html
* Incidents
  * file:///tmp/source-code/pom.xml
      * Line Number: 31
      * Message: 'Usage of JMS is not supported in Quarkus. It is recommended to use Quarkus' SmallRye Reactive Messaging instead of JMS.
 Replace the JavaEE/Jakarta JMS dependency with Smallrye Reactive:
 
 ```
 <dependency>
 <groupId>io.quarkus</groupId>
 <artifactId>quarkus-smallrye-reactive-messaging</artifactId>
 </dependency>
 
 ```
 
 Take a look at the Smallrye Reactive Connectors link below to know more about how to interact with different technologies (AMQP, Apache Camel, ...)'
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
### #1 - jms-to-reactive-quarkus-00010
* Category: mandatory
* Effort: 3
* Description: @MessageDriven - EJBs are not supported in Quarkus
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
      * Line Number: 14
      * Message: 'Enterprise Java Beans (EJBs) are not supported in Quarkus. CDI must be used.
 Please replace the `@MessageDriven` annotation with a CDI scope annotation like `@ApplicationScoped`.'
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
### #2 - jms-to-reactive-quarkus-00020
* Category: mandatory
* Effort: 3
* Description: Configure message listener method with @Incoming
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Incoming (SmallRye Reactive Messaging API): https://smallrye.io/smallrye-reactive-messaging/2.5.0/apidocs/org/eclipse/microprofile/reactive/messaging/Incoming.html
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
### #3 - jms-to-reactive-quarkus-00040
* Category: mandatory
* Effort: 3
* Description: JMS' Topic must be replaced with an Emitter
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Emitter (Microprofile Reactive Streams Messaging): https://smallrye.io/smallrye-reactive-messaging/2.0.2/apidocs/org/eclipse/microprofile/reactive/messaging/Emitter.html
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java
      * Line Number: 60
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
### #4 - jms-to-reactive-quarkus-00050
* Category: mandatory
* Effort: 5
* Description: JMS is not supported in Quarkus
* Labels: konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Quarkus - Guide: https://quarkus.io/guides
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/InventoryNotificationMDB.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java
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
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShoppingCartOrderProcessor.java
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
### #5 - persistence-to-quarkus-00000
* Category: optional
* Effort: 1
* Description: Move persistence config to a properties file
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Using Hibernate ORM and Jakarta persistence: https://quarkus.io/guides/hibernate-orm#persistence-xml
* Incidents
  * file:///tmp/source-code/src/main/resources/META-INF/persistence.xml
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
### #6 - persistence-to-quarkus-00011
* Category: potential
* Effort: 1
* Description: @Produces cannot annotate an EntityManager
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Setting up and configuring Hibernate ORM: https://quarkus.io/guides/hibernate-orm#setting-up-and-configuring-hibernate-orm
  * Using Hibernate ORM and Jakarta persistence: https://quarkus.io/guides/hibernate-orm#persistence-xml
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/persistence/Resources.java
      * Line Number: 5
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource. This makes having a `@Produces` annotation
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
 16          return em;
 17      }
 18  }

```
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/CatalogService.java
      * Line Number: 13
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource. This makes having a `@Produces` annotation
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
      * Line Number: 7
      * Message: 'In JavaEE/JakartaEE, using `@PersistenceContext` was needed in order to inject a data source. Quarkus, on the other hand,
 will create the bean automatically just by correctly setting up your datasource. This makes having a `@Produces` annotation
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
### #7 - remote-ejb-to-quarkus-00000
* Category: mandatory
* Effort: 1
* Description: Remote EJBs are not supported in Quarkus
* Labels: konveyor.io/source=jakarta-ee, konveyor.io/source=java-ee, konveyor.io/target=quarkus
* Links
  * Jakarta RESTful Web Services: https://jakarta.ee/specifications/restful-ws/
* Incidents
  * file:///tmp/source-code/src/main/java/com/redhat/coolstore/service/ShippingService.java
      * Line Number: 12
      * Message: 'Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:
 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path("<endpoint>")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.
 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.
 3. For every public method on the EJB being converted, do the following:
 - Annotate the method with `@jakarta.ws.rs.GET`
 - Annotate the method with `@jakarta.ws.rs.Path("<endpoint>")` and give it a proper endpoint path. As a rule of thumb, the method name can be used as endpoint, for instance:
 ```
 @Path("/increment")
 public void increment() 
 ```
 - Add `@jakarta.ws.rs.QueryParam("<param-name>")` to any method parameters if needed, where `<param-name>` is a name for the parameter.'
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
