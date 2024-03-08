# Mock a client doing client things
import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession("http://0.0.0.0:8080") as session:
        async with session.post("/dummy_json_request", json={"test": "object"}) as resp:
            print(resp.status)
            print(await resp.text())

        # x = {
        #   'application_name': 'another_app',
        #   'ruleset_name': 'cloud-readiness',
        #   'violation_name': 'java-rmi-00001',
        #   'incident_snip': "  1  /*\n  2   * JBoss, Home of Professional Open Source\n  3   * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual\n  4   * contributors by the @authors tag. See the copyright.txt in the\n  5   * distribution for a full listing of individual contributors.\n  6   *\n  7   * Licensed under the Apache License, Version 2.0 (the \"License\");\n  8   * you may not use this file except in compliance with the License.\n  9   * You may obtain a copy of the License at\n 10   * http://www.apache.org/licenses/LICENSE-2.0\n 11   * Unless required by applicable law or agreed to in writing, software\n 12   * distributed under the License is distributed on an \"AS IS\" BASIS,\n 13   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n 14   * See the License for the specific language governing permissions and\n 15   * limitations under the License.\n 16   */\n 17  package org.jboss.as.quickstarts.cmt.ejb;\n 18  \n 19  import java.rmi.RemoteException;\n 20  import java.util.List;\n 21  \n 22  import javax.ejb.EJBException;\n 23  import javax.ejb.Stateless;\n 24  import javax.ejb.TransactionAttribute;\n 25  import javax.ejb.TransactionAttributeType;\n 26  import javax.inject.Inject;\n 27  import javax.jms.JMSException;\n 28  import javax.naming.NamingException;\n 29  import javax.persistence.EntityManager;\n 30  import javax.persistence.PersistenceContext;\n 31  import javax.transaction.HeuristicMixedException;\n 32  import javax.transaction.HeuristicRollbackException;\n 33  import javax.transaction.NotSupportedException;\n 34  import javax.transaction.RollbackException;\n 35  import javax.transaction.SystemException;\n 36  \n 37  import org.jboss.as.quickstarts.cmt.model.Customer;\n 38  \n 39  @Stateless\n 40  public class CustomerManagerEJB {\n 41  \n 42      @PersistenceContext\n 43      private EntityManager entityManager;\n 44  \n 45      @Inject\n 46      private LogMessageManagerEJB logMessageManager;\n 47  \n 48      @Inject\n 49      private InvoiceManagerEJB invoiceManager;\n 50  \n 51      @TransactionAttribute(TransactionAttributeType.REQUIRED)\n 52      public void createCustomer(String name) throws RemoteException, JMSException {\n 53          logMessageManager.logCreateCustomer(name);\n 54  \n 55          Customer c1 = new Customer();\n 56          c1.setName(name);\n 57          entityManager.persist(c1);\n 58  \n 59          invoiceManager.createInvoice(name);\n 60  \n 61          // It could be done before all the 'storing' but this is just to show that\n 62          // the invoice is not delivered when we cause an EJBException\n 63          // after the fact but before the transaction is committed.\n 64          if (!nameIsValid(name)) {\n 65              throw new EJBException(\"Invalid name: customer names should only contain letters & '-'\");\n 66          }\n 67      }\n 68  \n 69      static boolean nameIsValid(String name) {\n 70          return name.matches(\"[\\\\p{L}-]+\");\n 71      }\n 72  \n 73      /**\n 74       * List all the customers.\n 75       *\n 76       * @return\n 77       * @throws NamingException\n 78       * @throws NotSupportedException\n 79       * @throws SystemException\n 80       * @throws SecurityException\n 81       * @throws IllegalStateException\n 82       * @throws RollbackException\n 83       * @throws HeuristicMixedException\n 84       * @throws HeuristicRollbackException\n 85       */\n 86      @TransactionAttribute(TransactionAttributeType.NEVER)\n 87      @SuppressWarnings(\"unchecked\")\n 88      public List<Customer> listCustomers() {\n 89          return entityManager.createQuery(\"select c from Customer c\").getResultList();\n 90      }\n 91  }\n",
        #   'incident_variables': {
        #       'file': 'file:///tmp/source-code/src/main/java/org/jboss/as/quickstarts/cmt/ejb/CustomerManagerEJB.java',
        #       'kind': 'Module',
        #       'name': 'java.rmi.RemoteException',
        #       'package': 'org.jboss.as.quickstarts.cmt.ejb',
        #   }
        # }
        # async with session.post('/get_incident_solution', json=x) as resp:
        #   print(resp.status)
        #   print(await resp.text())

        # input()

        # x = {
        #     "application_name": "another_app",
        #     "ruleset_name": "cloud-readiness",
        #     "violation_name": "java-rmi-00001",
        #     "incident_snip": '  1  /*\n  2   * JBoss, Home of Professional Open Source\n  3   * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual\n  4   * contributors by the @authors tag. See the copyright.txt in the\n  5   * distribution for a full listing of individual contributors.\n  6   *\n  7   * Licensed under the Apache License, Version 2.0 (the "License");\n  8   * you may not use this file except in compliance with the License.\n  9   * You may obtain a copy of the License at\n 10   * http://www.apache.org/licenses/LICENSE-2.0\n 11   * Unless required by applicable law or agreed to in writing, software\n 12   * distributed under the License is distributed on an "AS IS" BASIS,\n 13   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n 14   * See the License for the specific language governing permissions and\n 15   * limitations under the License.\n 16   */\n 17  package org.jboss.as.quickstarts.cmt.ejb;\n 18  \n 19  import java.rmi.RemoteException;\n 20  import java.util.List;\n 21  \n 22  import javax.ejb.EJBException;\n 23  import javax.ejb.Stateless;\n 24  import javax.ejb.TransactionAttribute;\n 25  import javax.ejb.TransactionAttributeType;\n 26  import javax.inject.Inject;\n 27  import javax.jms.JMSException;\n 28  import javax.naming.NamingException;\n 29  import javax.persistence.EntityManager;\n 30  import javax.persistence.PersistenceContext;\n 31  import javax.transaction.HeuristicMixedException;\n 32  import javax.transaction.HeuristicRollbackException;\n 33  import javax.transaction.NotSupportedException;\n 34  import javax.transaction.RollbackException;\n 35  import javax.transaction.SystemException;\n 36  \n 37  import org.jboss.as.quickstarts.cmt.model.Customer;\n 38  \n 39  @Stateless\n 40  public class CustomerManagerEJB {\n 41  \n 42      @PersistenceContext\n 43      private EntityManager entityManager;\n 44  \n 45      @Inject\n 46      private LogMessageManagerEJB logMessageManager;\n 47  \n 48      @Inject\n 49      private InvoiceManagerEJB invoiceManager;\n 50  \n 51      @TransactionAttribute(TransactionAttributeType.REQUIRED)\n 52      public void createCustomer(String name) throws RemoteException, JMSException {\n 53          logMessageManager.logCreateCustomer(name);\n 54  \n 55          Customer c1 = new Customer();\n 56          c1.setName(name);\n 57          entityManager.persist(c1);\n 58  \n 59          invoiceManager.createInvoice(name);\n 60  \n 61          // It could be done before all the \'storing\' but this is just to show that\n 62          // the invoice is not delivered when we cause an EJBException\n 63          // after the fact but before the transaction is committed.\n 64          if (!nameIsValid(name)) {\n 65              throw new EJBException("Invalid name: customer names should only contain letters & \'-\'");\n 66          }\n 67      }\n 68  \n 69      static boolean nameIsValid(String name) {\n 70          return name.matches("[\\\\p{L}-]+");\n 71      }\n 72  \n 73      /**\n 74       * List all the customers.\n 75       *\n 76       * @return\n 77       * @throws NamingException\n 78       * @throws NotSupportedException\n 79       * @throws SystemException\n 80       * @throws SecurityException\n 81       * @throws IllegalStateException\n 82       * @throws RollbackException\n 83       * @throws HeuristicMixedException\n 84       * @throws HeuristicRollbackException\n 85       */\n 86      @TransactionAttribute(TransactionAttributeType.NEVER)\n 87      @SuppressWarnings("unchecked")\n 88      public List<Customer> listCustomers() {\n 89          return entityManager.createQuery("select c from Customer c").getResultList();\n 90      }\n 91  }\n',
        #     "incident_variables": {
        #         "file": "file:///tmp/source-code/src/main/java/org/jboss/as/quickstarts/cmt/ejb/AnotherManagerEJB.java",
        #         "kind": "Module",
        #         "name": "java.rmi.RemoteException",
        #         "package": "org.jboss.as.quickstarts.cmt.ejb",
        #     },
        #     "file_name": "the/file/under/consideration.java",
        #     "file_contents": 'import System;\n\npublic static void main(string[] args){\nSystem.out.println("hello, world!");\n}\n',
        #     "line_number": 3,
        #     "analysis_message": "main function is too complicated!",
        # }

        x = {
            "application_name": "test_app",
            "violation_name": "jms-to-reactive-quarkus-00010",
            "ruleset_name": "kai/quarkus",
            "incident_snip": """  1  /*
  2   * JBoss, Home of Professional Open Source
  3   * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
  4   * contributors by the @authors tag. See the copyright.txt in the
  5   * distribution for a full listing of individual contributors.
  6   *
  7   * Licensed under the Apache License, Version 2.0 (the \"License\");
  8   * you may not use this file except in compliance with the License.
  9   * You may obtain a copy of the License at
 10   * http://www.apache.org/licenses/LICENSE-2.0
 11   * Unless required by applicable law or agreed to in writing, software
 12   * distributed under the License is distributed on an \"AS IS\" BASIS,
 13   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 14   * See the License for the specific language governing permissions and
 15   * limitations under the License.
 16   */
 17  package org.jboss.as.quickstarts.cmt.mdb;
 18  
 19  import java.util.logging.Logger;
 20  
 21  import javax.ejb.ActivationConfigProperty;
 22  import javax.ejb.MessageDriven;
 23  import javax.jms.JMSException;
 24  import javax.jms.Message;
 25  import javax.jms.MessageListener;
 26  import javax.jms.TextMessage;
 27  
 28  /**
 29   * <p>
 30   * A simple Message Driven Bean that asynchronously receives and processes the messages that are sent to the queue.
 31   * </p>
 32   *
 33   * @author Serge Pagop (spagop@redhat.com)
 34   *
 35   */
 36  @MessageDriven(name = \"HelloWorldMDB\", activationConfig = {
 37      @ActivationConfigProperty(propertyName = \"destinationType\", propertyValue = \"javax.jms.Queue\"),
 38      @ActivationConfigProperty(propertyName = \"destination\", propertyValue = \"queue/CMTQueue\"),
 39      @ActivationConfigProperty(propertyName = \"acknowledgeMode\", propertyValue = \"Auto-acknowledge\") })
 40  public class HelloWorldMDB implements MessageListener {
 41  
 42      private static final Logger logManager = Logger.getLogger(HelloWorldMDB.class.toString());
 43  
 44      /**
 45       * @see MessageListener#onMessage(Message)
 46       */
 47      public void onMessage(Message receivedMessage) {
 48          TextMessage textMsg = null;
 49          try {
 50              if (receivedMessage instanceof TextMessage) {
 51                  textMsg = (TextMessage) receivedMessage;
 52                  logManager.info(\"Received Message: \" + textMsg.getText());
 53              } else {
 54                  logManager.warning(\"Message of wrong type: \" + receivedMessage.getClass().getName());
 55              }
 56          } catch (JMSException ex) {
 57              throw new RuntimeException(ex);
 58          }
 59      }
 60  }""",
            "incident_variables": {
                "file": "file:///tmp/source-code/src/main/java/org/jboss/as/quickstarts/cmt/mdb/HelloWorldMDB.java",
                "kind": "Class",
                "name": "MessageDriven",
                "package": "org.jboss.as.quickstarts.cmt.mdb",
            },
            "file_name": "the/file/under/consideration.java",
            "file_contents": """  /*
   * JBoss, Home of Professional Open Source
   * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
   * contributors by the @authors tag. See the copyright.txt in the
   * distribution for a full listing of individual contributors.
   *
   * Licensed under the Apache License, Version 2.0 (the \"License\");
   * you may not use this file except in compliance with the License.
   * You may obtain a copy of the License at
   * http://www.apache.org/licenses/LICENSE-2.0
   * Unless required by applicable law or agreed to in writing, software
   * distributed under the License is distributed on an \"AS IS\" BASIS,
   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   * See the License for the specific language governing permissions and
   * limitations under the License.
   */
  package org.jboss.as.quickstarts.cmt.mdb;
  
  import java.util.logging.Logger;
  
  import javax.ejb.ActivationConfigProperty;
  import javax.ejb.MessageDriven;
  import javax.jms.JMSException;
  import javax.jms.Message;
  import javax.jms.MessageListener;
  import javax.jms.TextMessage;
  
  /**
   * <p>
   * A simple Message Driven Bean that asynchronously receives and processes the messages that are sent to the queue.
   * </p>
   *
   * @author Serge Pagop (spagop@redhat.com)
   *
   */
  @MessageDriven(name = \"HelloWorldMDB\", activationConfig = {
      @ActivationConfigProperty(propertyName = \"destinationType\", propertyValue = \"javax.jms.Queue\"),
      @ActivationConfigProperty(propertyName = \"destination\", propertyValue = \"queue/CMTQueue\"),
      @ActivationConfigProperty(propertyName = \"acknowledgeMode\", propertyValue = \"Auto-acknowledge\") })
  public class HelloWorldMDB implements MessageListener {
  
      private static final Logger logManager = Logger.getLogger(HelloWorldMDB.class.toString());
  
      /**
       * @see MessageListener#onMessage(Message)
       */
      public void onMessage(Message receivedMessage) {
          TextMessage textMsg = null;
          try {
              if (receivedMessage instanceof TextMessage) {
                  textMsg = (TextMessage) receivedMessage;
                  logManager.info(\"Received Message: \" + textMsg.getText());
              } else {
                  logManager.warning(\"Message of wrong type: \" + receivedMessage.getClass().getName());
              }
          } catch (JMSException ex) {
              throw new RuntimeException(ex);
          }
      }
  }""",
            "line_number": 36,
            "analysis_message": """Enterprise Java Beans (EJBs) are not supported in Quarkus. CDI must be used.
Please replace the `@MessageDriven` annotation with a CDI scope annotation like `@ApplicationScoped`.""",
        }

        async with session.post("/get_incident_solution", json=x) as resp:
            print(resp.status)

            # print(await resp.text())

            resp_json: dict = await resp.json()

            print(resp_json["llm_output"])


asyncio.run(main())
