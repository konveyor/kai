import os
import unittest

import yaml

from kai.incident_store import Application, IncidentStore


class TestIncidentStore(unittest.TestCase):

    def test_fetch_output_yaml_existing_app_output_yaml(self):
        # Test when the specified app folder and output.yaml exist
        i = IncidentStore()
        app_name = "helloworld-mdb"
        expected_output_yaml_path = os.path.join(
            "samples/analysis_reports", app_name, "solved/output.yaml"
        )
        self.assertEqual(i.fetch_output_yaml(app_name), expected_output_yaml_path)

    def test_fetch_output_yaml_non_existing_app(self):
        # Test when the specified app folder does not exist
        i = IncidentStore()
        app_name = "non_existing_app"
        yaml = i.fetch_output_yaml(app_name)
        self.assertIsNone(yaml)

    def test_update_cached_violations_no_incidents(self):
        # Test when there are no incidents in the report

        name = "sample"
        report = {
            "cloud-readiness": {
                "name": "cloud-readiness",
                "description": "This ruleset detects logging configurations that may be problematic when migrating an application to a cloud environment.",
                "violations": {
                    "session-00000": {
                        "description": "HTTP session replication (distributable web.xml)",
                        "category": "mandatory",
                        "labels": [
                            "clustering",
                            "konveyor.io/source=java",
                            "konveyor.io/source=java-ee",
                            "konveyor.io/target=cloud-readiness",
                        ],
                        "incidents": None,
                        "effort": 3,
                    }
                },
            }
        }

        a = Application(name, report)
        i = IncidentStore()
        i._update_cached_violations(a)
        # Assert that the cached_violations remains unchanged
        self.assertEqual(i.cached_violations["cloud-readiness"]["session-00000"], {})

    def test_update_cached_violations_with_incidents(self):
        # Test when there are incidents in the report

        name = "sample"
        report = {
            "cloud-readiness": {
                "name": "cloud-readiness",
                "description": "This ruleset detects logging configurations that may be problematic when migrating an application to a cloud environment.",
                "violations": {
                    "session-00000": {
                        "description": "HTTP session replication (distributable web.xml)",
                        "category": "mandatory",
                        "labels": [
                            "clustering",
                            "konveyor.io/source=java",
                            "konveyor.io/source=java-ee",
                            "konveyor.io/target=cloud-readiness",
                        ],
                        "incidents": [
                            {
                                "uri": "file:///tmp/source-code/webapp/WEB-INF/web.xml",
                                "message": "\n Session replication ensures that client sessions are not disrupted by node failure. Each node in the cluster shares information about ongoing sessions and can take over sessions if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.\n\n Recommendations\n\n * Review the session replication usage and ensure that it is configured properly.\n * Disable HTTP session clustering and accept its implications.\n * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.\n\n A remote data grid has the following benefits:\n\n * The application is more scaleable and elastic.\n * The application can survive EAP node failures because a JVM failure does not cause session data loss.\n * Session data can be shared by multiple applications.\n ",
                                "variables": {
                                    "data": "distributable",
                                    "innerText": "",
                                    "matchingXML": "",
                                },
                            }
                        ],
                        "effort": 3,
                    }
                },
            }
        }

        a = Application(name, report)
        i = IncidentStore()
        i._update_cached_violations(a)
        # Assert that the cached_violations is updated correctly
        expected_cached_violations = {
            "cloud-readiness": {
                "session-00000": {
                    "sample": {
                        "webapp/WEB-INF/web.xml": [
                            {
                                "variables": {
                                    "data": "distributable",
                                    "innerText": "",
                                    "matchingXML": "",
                                },
                                "line_number": None,
                                "message": "\n Session replication ensures that client sessions are not disrupted by node failure. Each node in the cluster shares information about ongoing sessions and can take over sessions if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.\n\n Recommendations\n\n * Review the session replication usage and ensure that it is configured properly.\n * Disable HTTP session clustering and accept its implications.\n * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.\n\n A remote data grid has the following benefits:\n\n * The application is more scaleable and elastic.\n * The application can survive EAP node failures because a JVM failure does not cause session data loss.\n * Session data can be shared by multiple applications.\n ",
                                "commitId": None,
                            }
                        ]
                    }
                }
            }
        }
        self.assertEqual(i.cached_violations, expected_cached_violations)

    def test_load_incidentstore_cached_violation(self):
        # Test when the specified app folder and output.yaml exist
        folder_path = "tests/test_data/sample"
        i = IncidentStore()

        i.load_incident_store(folder_path)
        self.assertIsNotNone(i.cached_violations)
        self.assertIsInstance(i.cached_violations, dict)
        self.assertEqual(len(i.cached_violations), 3)

        i.cleanup()

    def test_write_cached_violations(self):
        test_cached_violations = {
            "cloud-readiness": {
                "session-00000": {
                    "eap-coolstore-monolith": {
                        "webapp/WEB-INF/web.xml": [
                            {
                                "variables": {
                                    "data": "distributable",
                                    "innerText": "",
                                    "matchingXML": "",
                                },
                                "line_number": None,
                                "message": "\n Session replication ensures that client sessions are not disrupted by node failure. Each node in the cluster shares information about ongoing sessions and can take over sessions if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.\n\n Recommendations\n\n * Review the session replication usage and ensure that it is configured properly.\n * Disable HTTP session clustering and accept its implications.\n * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.\n\n A remote data grid has the following benefits:\n\n * The application is more scaleable and elastic.\n * The application can survive EAP node failures because a JVM failure does not cause session data loss.\n * Session data can be shared by multiple applications.\n ",
                            }
                        ]
                    }
                }
            },
            "localhost-http-00001": {
                "ticket-monster": {
                    "backend-v2/src/main/java/org/jboss/examples/ticketmonster/rest/BookingService.java": [
                        {
                            "variables": {
                                "matchingText": 'http://localhost:9090/rest/bookings"'
                            },
                            "line_number": 57,
                            "message": "The app is trying to access local resource by HTTP, please try to migrate the resource to cloud",
                        }
                    ],
                    "orders-service/src/test/java/org/ticketmonster/orders/SimpleTest.java": [
                        {
                            "variables": {"matchingText": "http://localhost"},
                            "line_number": 49,
                            "message": "The app is trying to access local resource by HTTP, please try to migrate the resource to cloud",
                        }
                    ],
                }
            },
            "localhost-jdbc-00002": {
                "ticket-monster": {
                    "orders-service/src/main/resources/application-mysql.properties": [
                        {
                            "variables": {
                                "matchingText": "jdbc:mysql://localhost:3306"
                            },
                            "line_number": 1,
                            "message": "The app is trying to access local resource by JDBC, please try to migrate the resource to cloud",
                        },
                        {
                            "variables": {
                                "matchingText": "jdbc:mysql://localhost:3306"
                            },
                            "line_number": 6,
                            "message": "The app is trying to access local resource by JDBC, please try to migrate the resource to cloud",
                        },
                    ],
                    "orders-service/target/classes/application-mysql.properties": [
                        {
                            "variables": {
                                "matchingText": "jdbc:mysql://localhost:3306"
                            },
                            "line_number": 1,
                            "message": "The app is trying to access local resource by JDBC, please try to migrate the resource to cloud",
                        },
                        {
                            "variables": {
                                "matchingText": "jdbc:mysql://localhost:3306"
                            },
                            "line_number": 6,
                            "message": "The app is trying to access local resource by JDBC, please try to migrate the resource to cloud",
                        },
                    ],
                }
            },
        }

        output_file_path = (
            "samples/generated_output/incident_store/test_cached_violations.yaml"
        )
        i = IncidentStore()
        try:
            # Call the function under test
            i.write_cached_violations(
                test_cached_violations, "test_cached_violations.yaml"
            )

            # Check if the file was created
            print(output_file_path)
            self.assertTrue(os.path.exists(output_file_path))

            # Check if the written datza matches the expected data
            with open(output_file_path, "r") as f:
                loaded_data = yaml.safe_load(f)
            self.assertEqual(loaded_data, test_cached_violations)

        finally:
            # Clean up
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

    def test_find_solved_issues(self):
        i = IncidentStore()
        i.load_incident_store("tests/test_data/sample")
        patches = i.get_solved_issue(
            "quarkus/springboot", "javaee-pom-to-quarkus-00010"
        )
        self.assertIsNotNone(patches)
        self.assertEquals(len(patches), 1)
        i.cleanup()

    def test_find_solved_issues_no_solved_issues(self):
        i = IncidentStore()
        i.load_incident_store("tests/test_data/sample")
        patches = i.get_solved_issue(
            "quarkus/springboot", "javaee-pom-to-quarkus-01010"
        )
        self.assertListEqual(patches, [])
        self.assertEquals(len(patches), 0)
        i.cleanup()

    def test_find_common_violations(self):
        i = IncidentStore()
        i.load_incident_store("tests/test_data/sample")
        violations = i.find_common_violations(
            "quarkus/springboot", "javaee-pom-to-quarkus-00010"
        )
        self.assertIsNotNone(violations)
        self.assertEquals(len(violations), 1)
        i.cleanup()

    if __name__ == "__main__":
        unittest.main()
