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

        x = {
            "application_name": "another_app",
            "ruleset_name": "cloud-readiness",
            "violation_name": "java-rmi-00001",
            "incident_snip": '  1  /*\n  2   * JBoss, Home of Professional Open Source\n  3   * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual\n  4   * contributors by the @authors tag. See the copyright.txt in the\n  5   * distribution for a full listing of individual contributors.\n  6   *\n  7   * Licensed under the Apache License, Version 2.0 (the "License");\n  8   * you may not use this file except in compliance with the License.\n  9   * You may obtain a copy of the License at\n 10   * http://www.apache.org/licenses/LICENSE-2.0\n 11   * Unless required by applicable law or agreed to in writing, software\n 12   * distributed under the License is distributed on an "AS IS" BASIS,\n 13   * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n 14   * See the License for the specific language governing permissions and\n 15   * limitations under the License.\n 16   */\n 17  package org.jboss.as.quickstarts.cmt.ejb;\n 18  \n 19  import java.rmi.RemoteException;\n 20  import java.util.List;\n 21  \n 22  import javax.ejb.EJBException;\n 23  import javax.ejb.Stateless;\n 24  import javax.ejb.TransactionAttribute;\n 25  import javax.ejb.TransactionAttributeType;\n 26  import javax.inject.Inject;\n 27  import javax.jms.JMSException;\n 28  import javax.naming.NamingException;\n 29  import javax.persistence.EntityManager;\n 30  import javax.persistence.PersistenceContext;\n 31  import javax.transaction.HeuristicMixedException;\n 32  import javax.transaction.HeuristicRollbackException;\n 33  import javax.transaction.NotSupportedException;\n 34  import javax.transaction.RollbackException;\n 35  import javax.transaction.SystemException;\n 36  \n 37  import org.jboss.as.quickstarts.cmt.model.Customer;\n 38  \n 39  @Stateless\n 40  public class CustomerManagerEJB {\n 41  \n 42      @PersistenceContext\n 43      private EntityManager entityManager;\n 44  \n 45      @Inject\n 46      private LogMessageManagerEJB logMessageManager;\n 47  \n 48      @Inject\n 49      private InvoiceManagerEJB invoiceManager;\n 50  \n 51      @TransactionAttribute(TransactionAttributeType.REQUIRED)\n 52      public void createCustomer(String name) throws RemoteException, JMSException {\n 53          logMessageManager.logCreateCustomer(name);\n 54  \n 55          Customer c1 = new Customer();\n 56          c1.setName(name);\n 57          entityManager.persist(c1);\n 58  \n 59          invoiceManager.createInvoice(name);\n 60  \n 61          // It could be done before all the \'storing\' but this is just to show that\n 62          // the invoice is not delivered when we cause an EJBException\n 63          // after the fact but before the transaction is committed.\n 64          if (!nameIsValid(name)) {\n 65              throw new EJBException("Invalid name: customer names should only contain letters & \'-\'");\n 66          }\n 67      }\n 68  \n 69      static boolean nameIsValid(String name) {\n 70          return name.matches("[\\\\p{L}-]+");\n 71      }\n 72  \n 73      /**\n 74       * List all the customers.\n 75       *\n 76       * @return\n 77       * @throws NamingException\n 78       * @throws NotSupportedException\n 79       * @throws SystemException\n 80       * @throws SecurityException\n 81       * @throws IllegalStateException\n 82       * @throws RollbackException\n 83       * @throws HeuristicMixedException\n 84       * @throws HeuristicRollbackException\n 85       */\n 86      @TransactionAttribute(TransactionAttributeType.NEVER)\n 87      @SuppressWarnings("unchecked")\n 88      public List<Customer> listCustomers() {\n 89          return entityManager.createQuery("select c from Customer c").getResultList();\n 90      }\n 91  }\n',
            "incident_variables": {
                "file": "file:///tmp/source-code/src/main/java/org/jboss/as/quickstarts/cmt/ejb/AnotherManagerEJB.java",
                "kind": "Module",
                "name": "java.rmi.RemoteException",
                "package": "org.jboss.as.quickstarts.cmt.ejb",
            },
            "file_name": "the/file/under/consideration.java",
            "file_contents": 'import System;\n\npublic static void main(string[] args){\nSystem.out.println("hello, world!");\n}\n',
            "line_number": 3,
            "analysis_message": "main function is too complicated!",
        }
        async with session.post("/get_incident_solution", json=x) as resp:
            print(resp.status)

            resp_json: dict = await resp.json()

            print(resp_json["prompt"])


asyncio.run(main())
