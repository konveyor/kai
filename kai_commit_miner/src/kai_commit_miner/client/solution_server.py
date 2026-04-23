"""HTTP client for pushing mined results to the solution server REST API."""

import json
import sys
from pathlib import Path

import httpx

from kai_commit_miner.classifier.models import (
    ClassificationResult,
    HintCandidate,
    RuleCandidate,
)
from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db.python_objects import SolutionFile


class SolutionServerClient:
    """Client for the solution server REST API."""

    def __init__(self, server_url: str, client_id: str) -> None:
        self.base_url = server_url.rstrip("/") + "/api/v1"
        self.client_id = client_id
        self._http = httpx.AsyncClient(base_url=self.base_url, timeout=60.0)

    async def close(self) -> None:
        await self._http.aclose()

    async def create_collection(
        self,
        name: str,
        description: str | None = None,
        source_repo: str | None = None,
        migration_type: str | None = None,
    ) -> int:
        """Create a collection and return its ID."""
        resp = await self._http.post(
            "/collections/",
            json={
                "name": name,
                "description": description,
                "source_repo": source_repo,
                "migration_type": migration_type,
                "metadata": {},
            },
        )
        resp.raise_for_status()
        return resp.json()["collection_id"]

    async def ingest_commit(
        self,
        incidents: list[ExtendedIncident],
        before_files: list[SolutionFile],
        after_files: list[SolutionFile],
        reasoning: str | None = None,
        collection_id: int | None = None,
    ) -> dict[str, int | list[int] | None]:
        """Atomically ingest a commit's worth of data."""
        resp = await self._http.post(
            "/bulk/ingest-commit",
            json={
                "client_id": self.client_id,
                "collection_id": collection_id,
                "incidents": [i.model_dump(mode="json") for i in incidents],
                "before_files": [f.model_dump(mode="json") for f in before_files],
                "after_files": [f.model_dump(mode="json") for f in after_files],
                "reasoning": reasoning,
            },
        )
        resp.raise_for_status()
        return resp.json()

    async def push_classification(
        self,
        result: ClassificationResult,
        collection_id: int | None = None,
    ) -> None:
        """Push a classification result to the solution server."""
        for hint in result.hints:
            if hint.skipped or not hint.sample_fixes:
                continue
            # Use the first sample fix as the representative incident + files
            fix = hint.sample_fixes[0]
            before_files = [SolutionFile(uri=fix.file_path, content=fix.before_content)]
            after_files = [SolutionFile(uri=fix.file_path, content=fix.after_content)]

            try:
                await self.ingest_commit(
                    incidents=[fix.incident],
                    before_files=before_files,
                    after_files=after_files,
                    reasoning=hint.hint_text,
                    collection_id=collection_id,
                )
            except Exception as e:
                print(f"Warning: failed to push hint: {e}", file=sys.stderr)


class DryRunClient:
    """Client that writes rich results to local JSON files instead of pushing to server."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._hints: list[dict] = []
        self._rule_candidates: list[dict] = []
        self._metadata: dict[str, object] = {}

    def set_metadata(self, key: str, value: object) -> None:
        self._metadata[key] = value

    async def close(self) -> None:
        (self.output_dir / "hints.json").write_text(json.dumps(self._hints, indent=2))
        (self.output_dir / "rule_candidates.json").write_text(
            json.dumps(self._rule_candidates, indent=2)
        )
        if self._metadata:
            (self.output_dir / "metadata.json").write_text(
                json.dumps(self._metadata, indent=2)
            )

    async def push_classification(
        self,
        result: ClassificationResult,
        collection_id: int | None = None,
    ) -> None:
        for hint in result.hints:
            sample_files = []
            for fix in hint.sample_fixes:
                sample_files.append(
                    {
                        "file_path": fix.file_path,
                        "incident_message": fix.incident.message,
                        "incident_uri": fix.incident.uri,
                        "incident_line": fix.incident.line_number,
                        "before_snippet": (
                            fix.before_snippet[:500] if fix.before_snippet else ""
                        ),
                        "after_snippet": (
                            fix.after_snippet[:500] if fix.after_snippet else ""
                        ),
                        "indirect": fix.indirect,
                    }
                )
            self._hints.append(
                {
                    "violation_key": hint.violation_key.model_dump(),
                    "hint_text": hint.hint_text,
                    "incident_count": hint.incident_count,
                    "skipped": hint.skipped,
                    "skipped_reason": hint.skipped_reason,
                    "sample_files": sample_files,
                }
            )
        for rc in result.rule_candidates:
            self._rule_candidates.append(rc.model_dump())
