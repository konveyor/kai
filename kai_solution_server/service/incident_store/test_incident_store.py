import datetime
import os
import shutil
import unittest
from typing import Callable

import git
import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from kai.analyzer_types import Report
from kai.constants import PATH_TEST_DATA
from kai.kai_config import (
    KaiConfigIncidentStore,
    KaiConfigIncidentStoreSQLiteArgs,
    KaiConfigModels,
)
from kai_solution_server.service.incident_store.backend import (
    incident_store_backend_factory,
)
from kai_solution_server.service.incident_store.incident_store import (
    Application,
    IncidentStore,
)
from kai_solution_server.service.incident_store.sql_types import (
    SQLAcceptedSolution,
    SQLApplication,
    SQLBase,
    SQLIncident,
    SQLRuleset,
    SQLViolation,
)
from kai_solution_server.service.llm_interfacing.model_provider import ModelProvider
from kai_solution_server.service.solution_handling.detection import (
    solution_detection_factory,
    solution_detection_naive,
)
from kai_solution_server.service.solution_handling.production import (
    SolutionProducerLLMLazy,
    SolutionProducerTextOnly,
)


class Fixture:
    @staticmethod
    def setUp(self: unittest.TestCase):
        pass

    @staticmethod
    def tearDown(self: unittest.TestCase):
        pass


def fixture(*fixtures: Fixture):
    def decorator(func: Callable):
        old_tearDown: Callable

        def new_tearDown(self):
            for fixture in reversed(fixtures):
                fixture.tearDown(self)

            self.__class__.tearDown = old_tearDown  # trunk-ignore(ruff/F821)

            old_tearDown(self)  # trunk-ignore(ruff/F821)

        def wrapper(*args, **kwargs):
            cls = args[0].__class__

            nonlocal old_tearDown
            if hasattr(cls, "tearDown"):
                old_tearDown = cls.tearDown
            else:
                old_tearDown = cls.tearDown

            cls.tearDown = new_tearDown

            for fixture in fixtures:
                fixture.setUp(args[0])

            func(*args, **kwargs)

        return wrapper

    return decorator


class BasicIncidentStore(Fixture):
    @staticmethod
    def setUp(self: unittest.TestCase):
        args = KaiConfigIncidentStoreSQLiteArgs(
            provider="sqlite",
            connection_string="sqlite:///:memory:",
        )

        backend = incident_store_backend_factory(args)
        solution_detector = solution_detection_naive
        solution_producer = SolutionProducerTextOnly()

        self.incident_store = IncidentStore(
            backend, solution_detector, solution_producer
        )

        self.incident_store.create_tables()


class FakeLLMIncidentStore(Fixture):
    @staticmethod
    def setUp(self: unittest.TestCase):
        args = KaiConfigIncidentStoreSQLiteArgs(
            provider="sqlite",
            connection_string="sqlite:///:memory:",
        )

        backend = incident_store_backend_factory(args)
        solution_detector = solution_detection_naive
        solution_producer = SolutionProducerLLMLazy(
            ModelProvider(
                KaiConfigModels(
                    provider="FakeListChatModel",
                    args={
                        "sleep": None,
                        "responses": [
                            "These are the steps:\n1. Frobinate the widget\n2. Profit\n",
                        ],
                    },
                )
            )
        )

        self.incident_store = IncidentStore(
            backend, solution_detector, solution_producer
        )
        self.incident_store.create_tables()


class GitRepo(Fixture):
    @staticmethod
    def setUp(self: unittest.TestCase):
        self.repo_path = PATH_TEST_DATA / "git_repo"
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)
        os.mkdir(PATH_TEST_DATA / "git_repo")
        self.repo = None

    @staticmethod
    def tearDown(self: unittest.TestCase):
        shutil.rmtree(self.repo_path)


class TestIncidentStore(unittest.TestCase):
    def check_number_of_entities(self, cls: SQLBase, expected: int, where_clause=None):
        with Session(self.incident_store.engine) as session:
            if where_clause:
                stmt = select(cls).where(where_clause)
            else:
                stmt = select(cls)

            result = len(session.scalars(stmt).all())
            self.assertTrue(
                result == expected,
                f"For {cls.__name__}, expected {expected}, got {result}",
            )

    def load_reports(self, folder_name: str, cases_to_load: list[str]):
        for case in cases_to_load:
            case_path = PATH_TEST_DATA / folder_name / case

            report = Report.load_report_from_file(case_path / "report.yaml")

            with open(case_path / "app.yaml", "r") as f:
                app_dict = yaml.safe_load(f.read())

            application = Application(
                app_dict["application_name"],
                app_dict["repo_uri_origin"],
                self.repo_path.as_uri(),
                app_dict["current_branch"],
                app_dict["current_commit"],
                datetime.datetime.fromtimestamp(app_dict["timestamp"]),
            )

            self.incident_store.load_report(application, report)

    @fixture(BasicIncidentStore, GitRepo)
    def test_load_report_no_incidents(self):
        self.repo = git.Repo.init(self.repo_path)
        self.repo.git.commit("--allow-empty", "-m", "Initial commit")

        with open(
            PATH_TEST_DATA / "test_load_report_no_incidents" / "report.yaml", "r"
        ) as f:
            report_object = yaml.safe_load(f.read())

        report = Report.load_report_from_object(report_object, 0)

        application = Application(
            "sample",
            self.repo_path.as_uri(),
            self.repo_path.as_uri(),
            "master",
            self.repo.head.commit.hexsha,
            datetime.datetime.now(),
        )

        self.incident_store.load_report(application, report)

        with Session(self.incident_store.engine) as session:
            incidents = session.query(SQLIncident).all()
            self.assertTrue(len(incidents) == 0)

    @fixture(BasicIncidentStore, GitRepo)
    def test_load_store(self):
        initial_report = Report.load_report_from_file(
            PATH_TEST_DATA / "test_load_store/initial/report.yaml"
        )
        solved_report = Report.load_report_from_file(
            PATH_TEST_DATA / "test_load_store/solved/report.yaml"
        )

        with open(PATH_TEST_DATA / "test_load_store/initial/app.yaml", "r") as f:
            initial_app_dict = yaml.safe_load(f.read())

        initial_application = Application(
            "helloworld-mdb",
            initial_app_dict["repo_uri_origin"],
            self.repo_path.as_uri(),
            initial_app_dict["current_branch"],
            initial_app_dict["current_commit"],
            datetime.datetime.fromtimestamp(initial_app_dict["timestamp"]),
        )

        with open(PATH_TEST_DATA / "test_load_store/solved/app.yaml", "r") as f:
            solved_app_dict = yaml.safe_load(f.read())

        solved_application = Application(
            "helloworld-mdb",
            solved_app_dict["repo_uri_origin"],
            self.repo_path.as_uri(),
            solved_app_dict["current_branch"],
            solved_app_dict["current_commit"],
            datetime.datetime.fromtimestamp(solved_app_dict["timestamp"]),
        )

        self.repo = git.Repo.clone_from(
            initial_app_dict["repo_uri_origin"], self.repo_path
        )

        self.incident_store.load_report(initial_application, initial_report)

        self.check_number_of_entities(SQLApplication, 1)
        self.check_number_of_entities(SQLRuleset, 23)
        self.check_number_of_entities(SQLViolation, 23)
        self.check_number_of_entities(SQLIncident, 74)
        self.check_number_of_entities(SQLAcceptedSolution, 0)

        self.incident_store.load_report(solved_application, solved_report)

        self.check_number_of_entities(SQLApplication, 1)
        self.check_number_of_entities(SQLRuleset, 23)
        self.check_number_of_entities(SQLViolation, 25)
        self.check_number_of_entities(SQLIncident, 77)
        self.check_number_of_entities(SQLAcceptedSolution, 39)

    @fixture(FakeLLMIncidentStore, GitRepo)
    def test_llm_summary_generation(self):
        def test_data_path():
            return PATH_TEST_DATA / "test_load_store"

        initial_report = Report.load_report_from_file(
            test_data_path() / "initial/report.yaml"
        )
        solved_report = Report.load_report_from_file(
            test_data_path() / "solved/report.yaml"
        )
        with open(test_data_path() / "initial/app.yaml", "r") as f:
            initial_app_dict = yaml.safe_load(f.read())

        initial_application = Application(
            "helloworld-mdb",
            initial_app_dict["repo_uri_origin"],
            self.repo_path.as_uri(),
            initial_app_dict["current_branch"],
            initial_app_dict["current_commit"],
            datetime.datetime.fromtimestamp(initial_app_dict["timestamp"]),
        )

        with open(test_data_path() / "solved/app.yaml", "r") as f:
            solved_app_dict = yaml.safe_load(f.read())

        solved_application = Application(
            "helloworld-mdb",
            solved_app_dict["repo_uri_origin"],
            self.repo_path.as_uri(),
            solved_app_dict["current_branch"],
            solved_app_dict["current_commit"],
            datetime.datetime.fromtimestamp(solved_app_dict["timestamp"]),
        )

        self.repo = git.Repo.clone_from(
            initial_app_dict["repo_uri_origin"], self.repo_path
        )

        self.incident_store.load_report(initial_application, initial_report)
        self.incident_store.load_report(solved_application, solved_report)

        queries: list[tuple] = []

        with Session(self.incident_store.engine) as session:
            solutions = session.query(SQLAcceptedSolution).all()
            for solution in solutions:
                self.assertTrue(solution.solution.llm_summary_generated is not None)
                self.assertTrue(solution.solution.llm_summary_generated is False)
                self.assertTrue(solution.solution.llm_summary is None)

                incident = solution.incidents[0]

                queries.append(
                    (
                        incident.ruleset_name,
                        incident.violation_name,
                        incident.incident_variables,
                        incident.incident_snip,
                    )
                )

        self.incident_store.post_process(limit=-1)

        for query in queries:
            solutions = self.incident_store.find_solutions(
                query[0], query[1], query[2], query[3]
            )

            for solution in solutions:
                self.assertTrue(solution.llm_summary_generated is True)
                self.assertTrue(solution.llm_summary is not None)
                self.assertTrue(isinstance(solution.llm_summary, str))
                self.assertTrue(len(solution.llm_summary) > 0)


@unittest.skip("Migrated old tests, need to be updated")
class TestIncidentStoreOld(unittest.TestCase):
    def setUp(self):
        # Initialize the IncidentStore
        self.folder_path = os.path.join(PATH_TEST_DATA, "sample")

        self.config = KaiConfigIncidentStore(
            solution_producers="text_only",
            solution_detectors="naive",
            args=KaiConfigIncidentStoreSQLiteArgs(
                provider="sqlite",
                connection_string="sqlite:///:memory:",
            ),
        )

        solution_detector = solution_detection_factory(self.config.solution_detectors)
        solution_producer = SolutionProducerTextOnly()

        self.incident_store = IncidentStore(
            self.config, solution_detector, solution_producer
        )

        self.report = Report()

        self.incident_store.load_incident_store()

    def tearDown(self):
        # Clean up after each test case
        self.incident_store.cleanup()

    def test_fetch_output_yaml_existing_app_output_yaml(self):
        # Test when the specified app folder and output.yaml exist
        app_name = "helloworld-mdb"
        expected_output_yaml_path = os.path.join(
            self.incident_store.analysis_dir, app_name, "solved/output.yaml"
        )
        self.assertEqual(
            self.incident_store.fetch_output_yaml(app_name), expected_output_yaml_path
        )

    def test_fetch_output_yaml_non_existing_app(self):
        # Test when the specified app folder does not exist
        app_name = "non_existing_app"
        yaml = self.incident_store.fetch_output_yaml(app_name)
        self.assertIsNone(yaml)

    def test_update_cached_violations_no_incidents(self):
        # Test when there are no incidents in the report
        self.incident_store.cached_violations = {}
        name = "sample"
        report = {"cloud-readiness": "blah"}

        a = Application(name, report)
        self.incident_store._update_cached_violations(a)
        # Assert that the cached_violations remains unchanged
        self.assertEqual(
            self.incident_store.cached_violations["cloud-readiness"]["session-00000"],
            {},
        )

    def test_update_cached_violations_with_incidents(self):
        # Test when there are incidents in the report
        self.incident_store.cached_violations = {}
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
        self.incident_store._update_cached_violations(a)

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
                            }
                        ]
                    }
                }
            }
        }
        self.assertEqual(
            self.incident_store.cached_violations, expected_cached_violations
        )

    def test_load_incidentstore_cached_violation(self):
        # Test when the specified app folder and output.yaml exist

        self.incident_store.load_incident_store()
        self.assertIsNotNone(self.incident_store.cached_violations)
        self.assertIsInstance(self.incident_store.cached_violations, dict)
        self.assertEqual(len(self.incident_store.cached_violations), 3)

        self.incident_store.cleanup()

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

        output_file_path = "tests/test_data/incident_store/test_cached_violations.yaml"
        try:
            # Call the function under test
            self.incident_store.write_cached_violations(
                test_cached_violations, "test_cached_violations.yaml"
            )

            # Check if the file was created
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
        self.incident_store.load_incident_store()
        patches = self.incident_store.get_solved_issue(
            "quarkus/springboot", "javaee-pom-to-quarkus-00010"
        )
        self.assertIsNotNone(patches)
        self.assertEqual(len(patches), 1)
        self.incident_store.cleanup()

    def test_find_solved_issues_no_solved_issues(self):
        self.incident_store.load_incident_store()
        patches = self.incident_store.get_solved_issue(
            "quarkus/springboot", "javaee-pom-to-quarkus-01010"
        )
        self.assertListEqual(patches, [])
        self.assertEqual(len(patches), 0)
        self.incident_store.cleanup()

    def test_find_common_violations(self):
        self.incident_store.load_incident_store()
        violations = self.incident_store.find_common_violations(
            "quarkus/springboot", "javaee-pom-to-quarkus-00010"
        )
        self.assertIsNotNone(violations)
        self.assertEqual(len(violations), 1)
        self.incident_store.cleanup()
