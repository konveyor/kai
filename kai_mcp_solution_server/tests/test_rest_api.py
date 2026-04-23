"""Tests for the REST API endpoints."""

import os
import unittest
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from kai_mcp_solution_server.resources import KaiSolutionServerContext, _SharedResources
from kai_mcp_solution_server.rest.app import create_rest_app
from kai_mcp_solution_server.settings import SolutionServerSettings

os.environ.setdefault("KAI_DB_DSN", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("KAI_LLM_PARAMS", '{"model":"fake"}')


async def _make_app() -> FastAPI:
    """Create a test app with initialized context on app.state."""
    # Reset shared resources so each test gets a fresh DB
    _SharedResources.initialized = False
    _SharedResources.engine = None
    _SharedResources.session_maker = None
    _SharedResources.model = None
    _SharedResources.db_semaphore = None
    _SharedResources.initialization_lock = None

    app = create_rest_app()
    settings = SolutionServerSettings()
    ctx = KaiSolutionServerContext(settings)
    await ctx.create()
    app.state.kai_ctx = ctx
    return app


class TestHealthEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_health(self) -> None:
        resp = await self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})

    async def test_ready(self) -> None:
        resp = await self.client.get("/ready")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ready")


class TestIncidentEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    def _make_incident(self, **overrides: object) -> dict:
        base = {
            "uri": "file:///src/main/java/com/example/Foo.java",
            "message": "javax import needs migration",
            "code_snip": "import javax.ejb.Stateless;",
            "line_number": 3,
            "variables": {},
            "ruleset_name": "quarkus/springboot",
            "ruleset_description": "Quarkus migration rules",
            "violation_name": "javax-to-jakarta-import",
            "violation_description": "Replace javax with jakarta",
            "violation_category": "mandatory",
            "violation_labels": [],
        }
        base.update(overrides)
        return base

    async def test_create_and_get_incident(self) -> None:
        incident = self._make_incident()
        resp = await self.client.post(
            "/incidents/",
            json={"client_id": "test", "extended_incident": incident},
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        incident_id = data["incident_id"]
        self.assertGreater(incident_id, 0)

        # Get it back
        resp = await self.client.get(f"/incidents/{incident_id}")
        self.assertEqual(resp.status_code, 200)
        detail = resp.json()
        self.assertEqual(detail["uri"], incident["uri"])
        self.assertEqual(detail["message"], incident["message"])
        self.assertEqual(detail["ruleset_name"], "quarkus/springboot")

    async def test_create_bulk_incidents(self) -> None:
        incidents = [
            self._make_incident(uri=f"file:///src/File{i}.java", line_number=i)
            for i in range(5)
        ]
        resp = await self.client.post(
            "/incidents/bulk",
            json={"client_id": "test", "extended_incidents": incidents},
        )
        self.assertEqual(resp.status_code, 201)
        results = resp.json()
        self.assertEqual(len(results), 5)

    async def test_list_incidents(self) -> None:
        # Create some incidents first
        for i in range(3):
            await self.client.post(
                "/incidents/",
                json={
                    "client_id": "test",
                    "extended_incident": self._make_incident(
                        uri=f"file:///src/File{i}.java"
                    ),
                },
            )

        resp = await self.client.get("/incidents/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 3)
        self.assertEqual(len(data["items"]), 3)

    async def test_list_incidents_with_filter(self) -> None:
        await self.client.post(
            "/incidents/",
            json={
                "client_id": "alice",
                "extended_incident": self._make_incident(),
            },
        )
        await self.client.post(
            "/incidents/",
            json={
                "client_id": "bob",
                "extended_incident": self._make_incident(uri="file:///other.java"),
            },
        )

        resp = await self.client.get("/incidents/", params={"client_id": "alice"})
        self.assertEqual(resp.json()["total"], 1)
        self.assertEqual(resp.json()["items"][0]["client_id"], "alice")

    async def test_get_nonexistent_incident(self) -> None:
        resp = await self.client.get("/incidents/9999")
        self.assertEqual(resp.status_code, 404)


class TestSolutionEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def _create_incident(self, client_id: str = "test") -> int:
        resp = await self.client.post(
            "/incidents/",
            json={
                "client_id": client_id,
                "extended_incident": {
                    "uri": "file:///src/Foo.java",
                    "message": "needs migration",
                    "code_snip": "import javax.ejb.Stateless;",
                    "line_number": 1,
                    "variables": {},
                    "ruleset_name": "quarkus/springboot",
                    "ruleset_description": "",
                    "violation_name": "javax-to-jakarta",
                    "violation_description": "",
                    "violation_category": "mandatory",
                    "violation_labels": [],
                },
            },
        )
        return resp.json()["incident_id"]

    async def test_create_and_get_solution(self) -> None:
        iid = await self._create_incident()

        resp = await self.client.post(
            "/solutions/",
            json={
                "client_id": "test",
                "incident_ids": [iid],
                "before": [
                    {"uri": "src/Foo.java", "content": "import javax.ejb.Stateless;"}
                ],
                "after": [
                    {"uri": "src/Foo.java", "content": "import jakarta.ejb.Stateless;"}
                ],
                "reasoning": "javax -> jakarta",
            },
        )
        self.assertEqual(resp.status_code, 201)
        solution_id = resp.json()["solution_id"]

        resp = await self.client.get(f"/solutions/{solution_id}")
        self.assertEqual(resp.status_code, 200)
        detail = resp.json()
        self.assertEqual(detail["reasoning"], "javax -> jakarta")
        self.assertEqual(len(detail["before"]), 1)
        self.assertEqual(len(detail["after"]), 1)
        self.assertEqual(len(detail["incidents"]), 1)

    async def test_list_solutions(self) -> None:
        iid = await self._create_incident()
        await self.client.post(
            "/solutions/",
            json={
                "client_id": "test",
                "incident_ids": [iid],
                "before": [{"uri": "a.java", "content": "old"}],
                "after": [{"uri": "a.java", "content": "new"}],
            },
        )

        resp = await self.client.get("/solutions/")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.json()["total"], 1)

    async def test_delete_solution(self) -> None:
        iid = await self._create_incident()
        resp = await self.client.post(
            "/solutions/",
            json={
                "client_id": "test",
                "incident_ids": [iid],
                "before": [{"uri": "a.java", "content": "old"}],
                "after": [{"uri": "a.java", "content": "new"}],
            },
        )
        solution_id = resp.json()["solution_id"]

        resp = await self.client.delete(
            f"/solutions/{solution_id}", params={"client_id": "test"}
        )
        self.assertEqual(resp.status_code, 200)

        resp = await self.client.get(f"/solutions/{solution_id}")
        self.assertEqual(resp.status_code, 404)


class TestViolationEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_list_violations(self) -> None:
        # Create an incident to auto-create the violation
        await self.client.post(
            "/incidents/",
            json={
                "client_id": "test",
                "extended_incident": {
                    "uri": "file:///a.java",
                    "message": "msg",
                    "code_snip": "code",
                    "line_number": 1,
                    "variables": {},
                    "ruleset_name": "rs1",
                    "ruleset_description": "ruleset one",
                    "violation_name": "v1",
                    "violation_description": "violation one",
                    "violation_category": "mandatory",
                    "violation_labels": [],
                },
            },
        )

        resp = await self.client.get("/violations/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["items"][0]["ruleset_name"], "rs1")
        self.assertEqual(data["items"][0]["violation_name"], "v1")

    async def test_get_violation_detail(self) -> None:
        await self.client.post(
            "/incidents/",
            json={
                "client_id": "test",
                "extended_incident": {
                    "uri": "file:///a.java",
                    "message": "msg",
                    "code_snip": "code",
                    "line_number": 1,
                    "variables": {},
                    "ruleset_name": "rs1",
                    "ruleset_description": "",
                    "violation_name": "v1",
                    "violation_description": "",
                    "violation_category": "mandatory",
                    "violation_labels": [],
                },
            },
        )

        resp = await self.client.get("/violations/rs1/v1")
        self.assertEqual(resp.status_code, 200)
        detail = resp.json()
        self.assertEqual(detail["incident_count"], 1)
        self.assertGreaterEqual(len(detail["incidents"]), 1)

    async def test_get_nonexistent_violation(self) -> None:
        resp = await self.client.get("/violations/fake/fake")
        self.assertEqual(resp.status_code, 404)


class TestCollectionEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_collection_crud(self) -> None:
        # Create
        resp = await self.client.post(
            "/collections/",
            json={
                "name": "coolstore-mining",
                "description": "Mining run on coolstore",
                "source_repo": "github.com/konveyor-ecosystem/coolstore",
                "migration_type": "javaee-to-quarkus",
            },
        )
        self.assertEqual(resp.status_code, 201)
        cid = resp.json()["collection_id"]

        # Get
        resp = await self.client.get(f"/collections/{cid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "coolstore-mining")
        self.assertEqual(resp.json()["solution_count"], 0)

        # List
        resp = await self.client.get("/collections/")
        self.assertEqual(resp.json()["total"], 1)

        # Update
        resp = await self.client.patch(
            f"/collections/{cid}",
            json={"description": "Updated description"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["description"], "Updated description")

        # Delete
        resp = await self.client.delete(f"/collections/{cid}")
        self.assertEqual(resp.status_code, 200)
        resp = await self.client.get(f"/collections/{cid}")
        self.assertEqual(resp.status_code, 404)

    async def test_add_items_to_collection(self) -> None:
        # Create a collection
        resp = await self.client.post("/collections/", json={"name": "test-col"})
        cid = resp.json()["collection_id"]

        # Create an incident + solution
        resp = await self.client.post(
            "/incidents/",
            json={
                "client_id": "test",
                "extended_incident": {
                    "uri": "file:///a.java",
                    "message": "msg",
                    "code_snip": "code",
                    "line_number": 1,
                    "variables": {},
                    "ruleset_name": "rs",
                    "ruleset_description": "",
                    "violation_name": "v",
                    "violation_description": "",
                    "violation_category": "mandatory",
                    "violation_labels": [],
                },
            },
        )
        iid = resp.json()["incident_id"]

        resp = await self.client.post(
            "/solutions/",
            json={
                "client_id": "test",
                "incident_ids": [iid],
                "before": [{"uri": "a.java", "content": "old"}],
                "after": [{"uri": "a.java", "content": "new"}],
            },
        )
        sid = resp.json()["solution_id"]

        # Add to collection
        resp = await self.client.post(
            f"/collections/{cid}/items",
            json={"solution_ids": [sid], "incident_ids": [iid]},
        )
        self.assertEqual(resp.status_code, 200)

        # Verify counts
        resp = await self.client.get(f"/collections/{cid}")
        self.assertEqual(resp.json()["solution_count"], 1)
        self.assertEqual(resp.json()["incident_count"], 1)


class TestBulkEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_ingest_commit(self) -> None:
        resp = await self.client.post(
            "/bulk/ingest-commit",
            json={
                "client_id": "miner",
                "incidents": [
                    {
                        "uri": "file:///src/Foo.java",
                        "message": "javax import",
                        "code_snip": "import javax.ejb.Stateless;",
                        "line_number": 1,
                        "variables": {},
                        "ruleset_name": "quarkus/springboot",
                        "ruleset_description": "",
                        "violation_name": "javax-to-jakarta",
                        "violation_description": "",
                        "violation_category": "mandatory",
                        "violation_labels": [],
                    },
                    {
                        "uri": "file:///src/Bar.java",
                        "message": "javax import",
                        "code_snip": "import javax.persistence.Entity;",
                        "line_number": 1,
                        "variables": {},
                        "ruleset_name": "quarkus/springboot",
                        "ruleset_description": "",
                        "violation_name": "javax-to-jakarta",
                        "violation_description": "",
                        "violation_category": "mandatory",
                        "violation_labels": [],
                    },
                ],
                "before_files": [
                    {"uri": "src/Foo.java", "content": "import javax.ejb.Stateless;"},
                    {
                        "uri": "src/Bar.java",
                        "content": "import javax.persistence.Entity;",
                    },
                ],
                "after_files": [
                    {"uri": "src/Foo.java", "content": "import jakarta.ejb.Stateless;"},
                    {
                        "uri": "src/Bar.java",
                        "content": "import jakarta.persistence.Entity;",
                    },
                ],
                "reasoning": "javax -> jakarta namespace migration",
            },
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(len(data["incident_ids"]), 2)
        self.assertGreater(data["solution_id"], 0)

    async def test_ingest_commit_with_collection(self) -> None:
        # Create collection first
        resp = await self.client.post("/collections/", json={"name": "test-mining-run"})
        cid = resp.json()["collection_id"]

        resp = await self.client.post(
            "/bulk/ingest-commit",
            json={
                "client_id": "miner",
                "collection_id": cid,
                "incidents": [
                    {
                        "uri": "file:///src/Foo.java",
                        "message": "javax import",
                        "code_snip": "import javax.ejb.Stateless;",
                        "line_number": 1,
                        "variables": {},
                        "ruleset_name": "quarkus/springboot",
                        "ruleset_description": "",
                        "violation_name": "javax-to-jakarta",
                        "violation_description": "",
                        "violation_category": "mandatory",
                        "violation_labels": [],
                    },
                ],
                "before_files": [
                    {"uri": "src/Foo.java", "content": "old"},
                ],
                "after_files": [
                    {"uri": "src/Foo.java", "content": "new"},
                ],
            },
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["collection_id"], cid)

        # Verify collection got updated
        resp = await self.client.get(f"/collections/{cid}")
        self.assertEqual(resp.json()["solution_count"], 1)
        self.assertEqual(resp.json()["incident_count"], 1)


class TestHintEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = await _make_app()
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=self.app), base_url="http://test"
        )

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_list_hints_empty(self) -> None:
        resp = await self.client.get("/hints/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["total"], 0)

    async def test_get_best_hint_empty(self) -> None:
        resp = await self.client.get(
            "/hints/best", params={"ruleset_name": "rs", "violation_name": "v"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json())

    async def test_get_nonexistent_hint(self) -> None:
        resp = await self.client.get("/hints/9999")
        self.assertEqual(resp.status_code, 404)
