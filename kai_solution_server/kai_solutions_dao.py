import json
import sqlite3
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class SolutionStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    UNKNOWN = "unknown"


@dataclass
class KaiSolution:
    id: int
    task: dict  # Store the entire task as JSON
    task_key: str  # Separate column for easy filtering
    before_code: Optional[str]
    after_code: Optional[str]
    diff: Optional[str]
    status: SolutionStatus


class KaiSolutionsDAO:
    """
    Data access object for the 'kai_solutions' table.
    This class encapsulates all DB operations.
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        conn is a live database connection. For production usage,
        you might want to manage concurrency, connection pooling, etc.
        """
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self._initialize_table()

    def _initialize_table(self) -> None:
        """
        Create table if it doesn't exist yet.
        """
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kai_solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_json TEXT NOT NULL,
                task_key TEXT NOT NULL,
                before_code TEXT,
                after_code TEXT,
                diff TEXT,
                status TEXT NOT NULL
            )
            """
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_kai_solutions_task_key ON kai_solutions(task_key)"
        )
        self.conn.commit()

    def create_solution(
        self, task: dict, before_code: str, after_code: str, diff: str, status: str
    ) -> int:
        """
        Insert a new Kai solution into the DB. Returns the new solution's ID.
        """
        if status not in [s.value for s in SolutionStatus]:
            status = SolutionStatus.UNKNOWN.value

        task_json = json.dumps(task)
        task_key = str(task.get("key", ""))

        cursor = self.conn.execute(
            """
            INSERT INTO kai_solutions (task_json, task_key, before_code, after_code, diff, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (task_json, task_key, before_code, after_code, diff, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_solution_status(self, solution_id: int, status: str) -> bool:
        """
        Update the status of a solution. Returns True if a record was updated.
        """
        if status not in [s.value for s in SolutionStatus]:
            status = SolutionStatus.UNKNOWN.value

        cursor = self.conn.execute(
            """
            UPDATE kai_solutions
               SET status = ?
             WHERE id = ?
            """,
            (status, solution_id),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_success_rate(self, task_key: str) -> float:
        """
        Return the fraction of solutions for this task_key that are "accepted."
        If none found, returns 0.0.
        """
        row_total = self.conn.execute(
            "SELECT COUNT(*) AS total FROM kai_solutions WHERE task_key = ?",
            (task_key,),
        ).fetchone()
        total = row_total["total"] if row_total else 0
        if total == 0:
            return 0.0

        row_accepted = self.conn.execute(
            """
            SELECT COUNT(*) AS accepted
            FROM kai_solutions
            WHERE task_key = ?
              AND status = ?
            """,
            (task_key, SolutionStatus.ACCEPTED.value),
        ).fetchone()
        accepted = row_accepted["accepted"] if row_accepted else 0

        return float(accepted) / float(total)

    def get_solution_history(self, task_key: str) -> list[KaiSolution]:
        """
        Return all solutions matching this task_key, as KaiSolution objects.
        """
        rows = self.conn.execute(
            """
            SELECT *
            FROM kai_solutions
            WHERE task_key = ?
            ORDER BY id ASC
            """,
            (task_key,),
        ).fetchall()

        solutions = []
        for row in rows:
            solutions.append(
                KaiSolution(
                    id=row["id"],
                    task=json.loads(row["task_json"]),
                    task_key=row["task_key"],
                    before_code=row["before_code"],
                    after_code=row["after_code"],
                    diff=row["diff"],
                    status=SolutionStatus(row["status"]),
                )
            )
        return solutions
