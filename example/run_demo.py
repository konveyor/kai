#!/usr/bin/env python

# Ensure that we have 'kai' in our import path
import json
import sys
from dataclasses import dataclass

import requests

sys.path.append("../../kai")

from kai import Report

SERVER_URL = "http://0.0.0.0:8080"


# TODOs
# 1) Add ConfigFile to tweak the server URL an rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in
# 3) Allow multiple violations to be fixed per request
# 4) Save the updated file to disk


@dataclass
class KaiRequestParams:
    application_name: str = ""
    file_name: str
    file_contents: str = ""
    violation_name: str
    ruleset_name: str
    analysis_message: str
    line_number: int | None = None
    incident_variables: dict | None = None
    incident_snip: str | None = None

    @staticmethod
    def from_incident(
        app_name, file_path, file_contents, incident
    ) -> "KaiRequestParams":
        return KaiRequestParams(
            appplication_name=app_name,
            file_name=file_path,
            file_contents=file_contents,
            violation_name=incident["violation_name"],
            ruleset_name=incident["ruleset_name"],
            analysis_message=incident["message"],
            line_number=incident["lineNumber"],  # this may be empty in the report
            incident_variables=incident["variables"],
            incident_snip="",  # We don't plan to use this
        )


def collect_parameters(file_path, violations) -> KaiRequestParams:
    # TODO need to translate file_path from analysis to where we keep sample apps
    # TODO need to read the file contents
    file_contents = ""
    # file_contents = open(file_path, "r").read()

    # TODO: Update for batching all incidents in a single request to backend
    # Limit to only 1 violation to begin with
    violation = violations[0]

    params = KaiRequestParams.from_incident(
        "NEED TO FIND APP NAME", file_path, file_contents, violation
    )

    # TODO remove hardcoded parameters
    ignored_params_delete_later = {
        "application_name": "test_app",
        "violation_name": "jms-to-reactive-quarkus-00010",
        "ruleset_name": "kai/quarkus",
        "incident_variables": {
            "file": "file:///tmp/source-code/src/main/java/org/jboss/as/quickstarts/cmt/mdb/HelloWorldMDB.java",
            "kind": "Class",
            "name": "MessageDriven",
            "package": "org.jboss.as.quickstarts.cmt.mdb",
        },
        "incident_snip": "",
        "file_name": "the/file/under/consideration.java",
        "line_number": 36,
        "analysis_message": """Enterprise Java Beans (EJBs) are not supported in Quarkus. CDI must be used.
Please replace the `@MessageDriven` annotation with a CDI scope annotation like `@ApplicationScoped`.""",
        "file_contents": """  
  /*
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
    }
    return params


def generate_fix(params):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    response = requests.post(
        f"{SERVER_URL}/get_incident_solution", data=json.dumps(params), headers=headers
    )
    print(response)
    return response


def parse_response(response):
    return ""


def run_demo(report):
    impacted_files = report.get_impacted_files()
    for file_path, violations in impacted_files.items():
        # TODO:  Check we have the correct file path
        # Gather the info we need to send to the REST API
        params = collect_parameters(file_path, violations)
        response = generate_fix(params)
        print(f"{response}\n")
        # updated_file_contents = parse_response(response)

        # Make the Request
        # Parse the Output
        # Write it to Disk
        # print(f"File: {file_path} has {len(violations)} violations.")

        # print("\n")
        return


if __name__ == "__main__":
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report(coolstore_analysis_dir)
    run_demo(r)
