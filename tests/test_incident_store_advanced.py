import subprocess  # trunk-ignore(bandit)
import time
import unittest

import psycopg2

from kai.incident_store import EmbeddingNone, PSQLIncidentStore


class TestIncidentStoreAdvanced(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the PostgreSQL container based on available runtime
        if cls.is_docker_available():
            cls.start_container_with_docker()
        elif cls.is_podman_available():
            cls.start_container_with_podman()
        else:
            raise RuntimeError("Neither Docker nor Podman is available.")

        # Wait for PostgreSQL to be ready
        cls.wait_for_postgres()

    @classmethod
    def start_container_with_docker(cls):
        subprocess.run(  # trunk-ignore(bandit)
            [
                "docker",
                "run",
                "-d",
                "--name",
                "kai_test",
                "-p",
                "5432:5432",
                "-e",
                "POSTGRES_USER=kai",
                "-e",
                "POSTGRES_PASSWORD=dog8code",
                "-e",
                "POSTGRES_DB=kai",
                "-v",
                "data:/var/lib/postgresql/data",
                "docker.io/pgvector/pgvector:pg15",
            ]
        )

    @classmethod
    def start_container_with_podman(cls):
        subprocess.run(  # trunk-ignore(bandit)
            [
                "podman",
                "run",
                "-d",
                "--name",
                "kai_test",
                "-p",
                "5432:5432",
                "-e",
                "POSTGRES_USER=kai",
                "-e",
                "POSTGRES_PASSWORD=dog8code",
                "-e",
                "POSTGRES_DB=kai",
                "-v",
                "data:/var/lib/postgresql/data",
                "docker.io/pgvector/pgvector:pg15",
            ]
        )

    @classmethod
    def is_docker_available(cls):
        return (
            subprocess.run(  # trunk-ignore(bandit)
                ["docker", "--version"], capture_output=True
            ).returncode
            == 0
        )

    @classmethod
    def is_podman_available(cls):
        return (
            subprocess.run(  # trunk-ignore(bandit)
                ["podman", "--version"], capture_output=True
            ).returncode
            == 0
        )

    @classmethod
    def wait_for_postgres(cls):
        conn = None
        attempts = 0
        while conn is None and attempts < 10:
            try:
                conn = psycopg2.connect(  # trunk-ignore(bandit)
                    dbname="kai",
                    user="kai",
                    password="dog8code",
                    host="localhost",
                    port=5432,
                )
            except psycopg2.OperationalError:
                attempts += 1
                time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        # Stop and remove the PostgreSQL container based on available runtime
        if cls.is_docker_available():
            subprocess.run(["docker", "stop", "kai_test"])  # trunk-ignore(bandit)
            subprocess.run(["docker", "rm", "kai_test"])  # trunk-ignore(bandit)
        elif cls.is_podman_available():
            subprocess.run(["podman", "stop", "kai_test"])  # trunk-ignore(bandit)
            subprocess.run(["podman", "rm", "kai_test"])  # trunk-ignore(bandit)

    def test_database_connection(self):
        # Test database connection
        conn = psycopg2.connect(  # trunk-ignore(bandit)
            dbname="kai", user="kai", password="dog8code", host="localhost", port=5432
        )
        self.assertIsNotNone(conn)
        conn.close()

    def create_instance(self):
        psqlis = PSQLIncidentStore(
            config_filepath="tests/test_data/data/database.toml",
            config_section="postgresql",
            emb_provider=EmbeddingNone(),
            drop_tables=True,
        )
        return psqlis

    def test_create_instance(self):
        psqlis = self.create_instance()
        self.assertIsNotNone(psqlis)

    def test_load_store(self):
        psqlis = self.create_instance()
        self.assertIsNotNone(psqlis)
        psqlis.load_store("tests/test_data/sample")
        # Connect to the database
        conn = psycopg2.connect(  # trunk-ignore(bandit)
            dbname="kai", user="kai", password="dog8code", host="localhost", port=5432
        )
        cursor = conn.cursor()

        # Execute a query to count the number of rows in a table
        cursor.execute("SELECT COUNT(*) FROM applications;")
        count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM incidents;")
        incidents_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM rulesets;")
        rulesets_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM accepted_solutions;")
        accepted_solutions_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        self.assertTrue(count == 1, "Database should have 1 app")
        self.assertTrue(incidents_count > 0, "Database should have incidents")
        self.assertTrue(rulesets_count > 0, "Database should have rulesets")
        self.assertTrue(
            accepted_solutions_count > 0, "Database should have accepted_solutions"
        )


if __name__ == "__main__":
    unittest.main()
