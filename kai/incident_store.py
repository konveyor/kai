import argparse
import datetime
import json
import os
import tomllib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from inspect import signature
from typing import Literal, Optional
from urllib.parse import unquote, urlparse

import psycopg2
import yaml
from git import Repo
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor, DictRow

from kai.embedding_provider import EmbeddingNone, EmbeddingProvider
from kai.kai_logging import KAI_LOG
from kai.report import Report

BASE_PATH = os.path.dirname(__file__)


class IncidentStore(ABC):

    @abstractmethod
    def load_store(path: str):
        pass

    @abstractmethod
    def delete_store():
        pass

    @abstractmethod
    def add_incident():
        pass

    @abstractmethod
    def find_similar_incident(
        violation_name: str,
        ruleset_name: str,
        incident_snip: str,
        incident_vars: dict,
    ) -> tuple[
        Optional[dict],
        Literal[
            "exact",
            "variables_mismatch",
            "similarity_only",
            "unseen_violation",
            "ambiguous_violation",
        ],
    ]:
        """
        Returns tuple[dict | None, str] - First element is the match if it exists
        - Second element is whether it is an exact match or not. Values can be:
          - 'exact': exact match. From the same violation and has the same
            variables. Filtered using similarity search
          - 'variables_mismatch': From the same violation but does not have the same
            variables.
          - 'similarity_only': Not from the same violation, only based on snip
            similarity search
          - 'unseen_violation': We haven't seen this violation before. Same result
            as 'similarity_only'
          - 'ambiguous_violation': violation_name and ruleset_name did not uniquely
            identify a violation. Same result as 'similarity_only'
        """
        pass


@dataclass
class Application:
    application_id: int | None
    application_name: str
    repo_uri_origin: str
    repo_uri_local: str
    current_branch: str
    current_commit: str
    generated_at: datetime.datetime

    def as_tuple(self):
        return (
            self.application_id,
            self.application_name,
            self.repo_uri_origin,
            self.repo_uri_local,
            self.current_branch,
            self.current_commit,
            self.generated_at,
        )

    @staticmethod
    def from_dict_row(row: DictRow) -> "Application":
        return Application(
            application_id=row["application_id"],
            application_name=row["application_name"],
            repo_uri_origin=row["repo_uri_origin"],
            repo_uri_local=row["repo_uri_local"],
            current_branch=row["current_branch"],
            current_commit=row["current_commit"],
            generated_at=row["generated_at"],
        )


def supply_cursor_if_none(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        sig = signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        if "cur" not in bound_args.arguments or bound_args.arguments["cur"] is None:
            with self.conn.cursor() as cur:
                bound_args.arguments["cur"] = cur
                return func(*bound_args.args, **bound_args.kwargs)
        else:
            return func(*bound_args.args, **bound_args.kwargs)

    return wrapper


# TODO: Potentially create a Redis version of the incident store as well?


# TODO(@JonahSussman): Migrate this to use an ORM
class PSQLIncidentStore(IncidentStore):
    def __init__(
        self,
        *,
        drop_tables: bool = False,
        config_filepath: str = None,
        config_section: str = None,
        config: dict = None,
        emb_provider: EmbeddingProvider = None,
    ):
        # Config parsing. Either comes from a dict or a .toml file
        cf_none = config_filepath is None
        cs_none = config_section is None
        cd_none = config is None

        if cf_none != cs_none:
            raise Exception(
                "config_filepath and config_section must both be set if using .ini file."
            )
        if not (cf_none ^ cd_none):
            raise Exception("Must provide either config .toml or config dict.")

        if not cf_none:
            with open(config_filepath, "rb") as f:
                config = tomllib.load(f)

            if config_section not in config:
                raise Exception(
                    f"Section {config_section} not found in file {config_filepath}"
                )

            config = config[config_section]

        # Embedding provider
        if emb_provider is None:
            raise Exception("emb_provider must not be None")

        self.emb_provider = emb_provider

        try:
            with psycopg2.connect(cursor_factory=DictCursor, **config) as conn:
                KAI_LOG.info("Connected to the PostgreSQL server.")
                self.conn: connection = conn
                self.conn.autocommit = True

            with self.conn.cursor() as cur:
                # TODO: Figure out portable way to install the pgvector extension.
                # Containerize? "CREATE EXTENSION IF NOT EXISTS vector;" Only works as
                # superuser

                # TODO: along with analyzer_types.py, we should really use something
                # like openapi to nail down the spec and autogenerate the types

                if drop_tables:
                    cur.execute(
                        open(f"{BASE_PATH}/data/sql/drop_tables.sql", "r").read()
                    )

                cur.execute(open(f"{BASE_PATH}/data/sql/create_tables.sql", "r").read())

                dim = self.emb_provider.get_dimension()
                for q in open(
                    f"{BASE_PATH}/data/sql/add_embedding.sql", "r"
                ).readlines():
                    cur.execute(q, (dim,))

        except (psycopg2.DatabaseError, Exception) as error:
            KAI_LOG.error(f"Error initializing PSQLIncidentStore: {error}")

    @supply_cursor_if_none
    def select_application(
        self, app_id: int, app_name: str = None, cur: DictCursor = None
    ) -> list[DictRow]:
        if app_id is None and app_name is None:
            return []

        if app_id is not None:
            cur.execute(
                "SELECT * FROM applications WHERE application_id = %s;", (app_id,)
            )
        elif app_name is not None:
            cur.execute(
                "SELECT * FROM applications WHERE application_name = %s;", (app_name,)
            )
        else:
            raise Exception("At least one of app_id or app_name must be not None.")

        # return [Application.from_dict_row(row) for row in cur.fetchall()]
        return cur.fetchall()

    @supply_cursor_if_none
    def insert_application(self, app: Application, cur: DictCursor = None) -> DictRow:
        cur.execute(
            """INSERT INTO applications(application_name, repo_uri_origin, repo_uri_local, current_branch, current_commit, generated_at)
      VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;""",
            app.as_tuple()[1:],
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def update_application(
        self, application_id: int, app: Application, cur: DictCursor = None
    ) -> DictRow:
        cur.execute(
            """UPDATE applications
      SET application_name = %s,
        repo_uri_origin = %s,
        repo_uri_local = %s,
        current_branch = %s,
        current_commit = %s,
        generated_at = %s
      WHERE application_id = %s
      RETURNING *;""",
            (
                app.application_name,
                app.repo_uri_origin,
                app.repo_uri_local,
                app.current_branch,
                app.current_commit,
                app.generated_at,
                application_id,
            ),
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def select_ruleset(
        self, ruleset_id: int = None, ruleset_name: str = None, cur: DictCursor = None
    ) -> list[DictRow]:
        # def select_ruleset(self, ruleset_id: int = None, ruleset_name: str = None, application_id: int = None, cur: DictCursor = None) -> list[DictRow]:
        if ruleset_id is not None:
            cur.execute("SELECT * FROM rulesets WHERE ruleset_id = %s;", (ruleset_id,))
        # elif ruleset_name is not None and application_id is not None:
        elif ruleset_name is not None:
            cur.execute(
                # "SELECT * FROM rulesets WHERE ruleset_name = %s AND application_id = %s;",
                "SELECT * FROM rulesets WHERE ruleset_name = %s;",
                # (ruleset_name, application_id,)
                (ruleset_name,),
            )
        else:
            raise Exception(
                "At least one of ruleset_id or ruleset_name must be not None."
            )

        return cur.fetchall()

    @supply_cursor_if_none
    def insert_ruleset(
        self, ruleset_name: str, tags: list[str], cur: DictCursor = None
    ) -> DictRow:
        # def insert_ruleset(self, ruleset_name: str, application_id: int, tags: list[str], cur: DictCursor = None) -> DictRow:
        cur.execute(
            # """INSERT INTO rulesets(ruleset_name, application_id, tags)
            """INSERT INTO rulesets(ruleset_name, tags)
      VALUES (%s, %s) RETURNING*;""",
            # VALUES (%s, %s, %s) RETURNING*;""",
            # (ruleset_name, application_id, json.dumps(tags))
            (ruleset_name, json.dumps(tags)),
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def select_violation(
        self,
        violation_id: int = None,
        violation_name: str = None,
        ruleset_id: int = None,
        cur: DictCursor = None,
    ) -> list[DictRow]:
        if violation_id is not None:
            cur.execute(
                "SELECT * FROM violations WHERE violation_id = %s;", (violation_id,)
            )
        elif violation_name is not None and ruleset_id is not None:
            cur.execute(
                "SELECT * FROM violations WHERE violation_name = %s AND ruleset_id = %s;",
                (
                    violation_name,
                    ruleset_id,
                ),
            )
        else:
            raise Exception(
                "At least one of violation_id or (violation_name, ruleset_id) must be not None."
            )

        return cur.fetchall()

    @supply_cursor_if_none
    def insert_violation(
        self,
        violation_name: str,
        ruleset_id: int,
        category: str,
        labels: list[str],
        cur: DictCursor = None,
    ) -> DictRow:
        cur.execute(
            """INSERT INTO violations(violation_name, ruleset_id, category, labels)
      VALUES (%s, %s, %s, %s) RETURNING *;""",
            (violation_name, ruleset_id, category, json.dumps(sorted(labels))),
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def insert_incident(
        self,
        violation_id: int,
        application_id: int,
        incident_uri: str,
        incident_snip: str,
        incident_line: int,
        incident_variables: dict,
        solution_id: int = None,
        cur: DictCursor = None,
    ) -> DictRow:
        # if isinstance(incident_variables, str):
        #   incident_variables = json.loads(incident_variables)
        # if not isinstance(incident_variables, list):
        #   raise Exception(f"incident_variables must be of type list. Got type '{type(incident_variables)}'")

        vars_str = json.dumps(incident_variables)
        truncated_vars = (vars_str[:75] + "...") if len(vars_str) > 75 else vars_str

        KAI_LOG.info(
            f"Inserting incident {(violation_id, application_id, incident_uri, incident_line, truncated_vars, solution_id,)}"
        )

        cur.execute(
            """INSERT INTO incidents(violation_id, application_id, incident_uri, incident_snip, incident_line, incident_variables, solution_id, incident_snip_embedding)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
            (
                violation_id,
                application_id,
                incident_uri,
                incident_snip,
                incident_line,
                json.dumps(incident_variables),
                solution_id,
                str(self.emb_provider.get_embedding(incident_snip)),
            ),
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def insert_accepted_solution(
        self,
        generated_at: datetime.datetime,
        solution_big_diff: str,
        solution_small_diff: str,
        solution_original_code: str,
        solution_updated_code: str,
        cur: DictCursor = None,
    ):
        KAI_LOG.info(f"Inserting accepted solution {((generated_at))}")
        small_diff_embedding = str(self.emb_provider.get_embedding(solution_small_diff))
        original_code_embedding = str(
            self.emb_provider.get_embedding(solution_original_code)
        )

        # Encode the strings using the appropriate encoding method
        # to avoid unicode errors TODO: validate if this is the right way to do it
        solution_big_diff = solution_big_diff.encode("utf-8", "ignore").decode("utf-8")
        solution_small_diff = solution_small_diff.encode("utf-8", "ignore").decode(
            "utf-8"
        )
        solution_original_code = solution_original_code.encode(
            "utf-8", "ignore"
        ).decode("utf-8")
        solution_updated_code = solution_updated_code.encode("utf-8", "ignore").decode(
            "utf-8"
        )

        cur.execute(
            """INSERT INTO accepted_solutions(generated_at, solution_big_diff,
      solution_small_diff, solution_original_code, solution_updated_code,
      small_diff_embedding, original_code_embedding)
      VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
            (
                generated_at,
                solution_big_diff,
                solution_small_diff,
                solution_original_code,
                solution_updated_code,
                small_diff_embedding,
                original_code_embedding,
            ),
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def select_accepted_solution(self, solution_id: int, cur: DictCursor = None):
        cur.execute(
            "SELECT * FROM accepted_solutions WHERE solution_id = %s;", (solution_id,)
        )

        return cur.fetchone()

    @supply_cursor_if_none
    def get_fuzzy_similar_incident(
        self,
        violation_name: str,
        ruleset_name: str,
        incident_snip: str,
        incident_vars: dict,
        cur: DictCursor = None,
    ):
        """
        Returns tuple[DictRow | None, str] - First element is the match if it exists
        - Second element is whether it is an exact match or not. Values can be:
          - 'exact': exact match. From the same violation and has the same
            variables. Filtered using similarity search
          - 'variables_mismatch': From the same violation but does not have the same
            variables.
          - 'similarity_only': Not from the same violation, only based on snip
            similarity search
          - 'unseen_violation': We haven't seen this violation before. Same result
            as 'similarity_only'
          - 'ambiguous_violation': violation_name and ruleset_name did not uniquely
            identify a violation. Same result as 'similarity_only'
        """

        # # Pseudo-code
        # this_violation = get_violation_from_params()
        # if this_violation_dne:
        #   return get_snip_with_highest_embedding_similarity_from_all_violations(), 'similarity_only'

        # this_violation_slns = get_solutions_for_this_violation()

        # if len(this_violation_slns) == 0:
        #   return get_snip_with_highest_embedding_similarity_from_all_violations(), 'similarity_only'

        # # The violation we are looking at has at least one solution
        # filter_on_vars = this_violation_slns.filter_exact(inp_vars)

        # if len(filter_on_vars) == 0:
        #   return get_snip_with_highest_embedding_similarity_from_all_solutions(), 'variables_mismatch'
        # if len(filter_on_vars) == 1:
        #   return filter_on_vars[0], 'exact'
        # if len(filter_on_vars) > 1:
        #   return get_snip_with_highest_embedding_similarity_from_filtered_set(), 'exact'

        KAI_LOG.debug("get_fuzzy_similar_incident")

        emb = self.emb_provider.get_embedding(incident_snip)
        emb_str = str(emb)

        incident_vars_str = json.dumps(incident_vars)

        def highest_embedding_similarity_from_all():
            cur.execute(
                """
                SELECT * 
                FROM incidents 
                WHERE solution_id IS NOT NULL
                ORDER BY incident_snip_embedding <-> %s LIMIT 1;""",
                (emb_str,),
            )
            return dict(cur.fetchone())

        cur.execute(
            """
      SELECT v.*
      FROM violations v
      JOIN rulesets r ON v.ruleset_id = r.ruleset_id
      WHERE v.violation_name = %s
      AND r.ruleset_name = %s;
      """,
            (violation_name, ruleset_name),
        )

        violation_query = cur.fetchall()

        if len(violation_query) > 1:
            KAI_LOG.info("Ambiguous violation based on ruleset_name and violation_name")
            return highest_embedding_similarity_from_all(), "ambiguous_violation"
        if len(violation_query) == 0:
            KAI_LOG.info(f"No violations matched: {ruleset_name=} {violation_name=}")
            return highest_embedding_similarity_from_all(), "unseen_violation"

        violation = violation_query[0]

        cur.execute(
            """
      SELECT COUNT(*)
      FROM incidents
      WHERE violation_id = %s
      AND solution_id IS NOT NULL;
      """,
            (violation["violation_id"],),
        )

        number_of_slns = cur.fetchone()[0]
        if number_of_slns == 0:
            KAI_LOG.info(
                f"No solutions for violation: {ruleset_name=} {violation_name=}"
            )
            return highest_embedding_similarity_from_all(), "similarity_only"

        cur.execute(
            """
      SELECT *
      FROM incidents
      WHERE violation_id = %s
      AND solution_id IS NOT NULL
      AND incident_variables <@ %s
      AND incident_variables @> %s;
      """,
            (violation["violation_id"], incident_vars_str, incident_vars_str),
        )

        exact_variables_query = cur.fetchall()

        if len(exact_variables_query) == 1:
            return dict(exact_variables_query[0]), "exact"
        elif len(exact_variables_query) == 0:
            cur.execute(
                """
        SELECT *
        FROM incidents
        WHERE violation_id = %s
        AND solution_id IS NOT NULL
        ORDER BY incident_snip_embedding <-> %s
        LIMIT 1;
        """,
                (
                    violation["violation_id"],
                    emb_str,
                ),
            )
            return dict(cur.fetchone()), "variables_mismatch"
        else:
            cur.execute(
                """
        SELECT *
        FROM incidents
        WHERE violation_id = %s
        AND solution_id IS NOT NULL
        AND incident_variables <@ %s
        AND incident_variables @> %s
        ORDER BY incident_snip_embedding <-> %s
        LIMIT 1;
        """,
                (
                    violation["violation_id"],
                    incident_vars_str,
                    incident_vars_str,
                    emb_str,
                ),
            )
            return dict(cur.fetchone()), "exact"

    def insert_and_update_from_report(self, app: Application, report: Report):
        """
        Returns: (number_new_incidents, number_unsolved_incidents,
        number_solved_incidents): tuple[int, int, int]
        """
        # FIXME: Only does stuff within the same application. Maybe fixed?

        # create entries if not exists
        # reference the old-new matrix
        #           old
        #         | NO     | YES
        # --------|--------+-----------------------------
        # new NO  | -      | update (SOLVED, embeddings)
        #     YES | insert | update (line number, etc...)

        repo_path = unquote(urlparse(app.repo_uri_local).path)
        repo = Repo(repo_path)
        old_commit: str
        new_commit = app.current_commit

        number_new_incidents = 0
        number_unsolved_incidents = 0
        number_solved_incidents = 0

        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS incidents_temp;")
            cur.execute("CREATE TABLE incidents_temp (LIKE incidents INCLUDING ALL);")

            query_app = self.select_application(
                app.application_id, app.application_name, cur
            )

            if len(query_app) >= 2:
                raise Exception(f"Multiple applications found for {app}.")
            elif len(query_app) == 0 and app.application_id is not None:
                raise Exception(
                    f"No application with application_id {app.application_id}."
                )
            elif len(query_app) == 0:
                application = self.insert_application(app, cur)
            else:
                application = query_app[0]

            old_commit = application["current_commit"]

            report_dict = report.get_report()

            for ruleset_name, ruleset_dict in report_dict.items():
                query_ruleset = self.select_ruleset(
                    ruleset_name=ruleset_name,
                    # application_id=application['application_id'],
                    cur=cur,
                )

                if len(query_ruleset) >= 2:
                    raise Exception("Multiple rulesets found.")
                elif len(query_ruleset) == 0:
                    ruleset = self.insert_ruleset(
                        ruleset_name=ruleset_name,
                        # application_id=application['application_id'],
                        tags=ruleset_dict.get("tags", []),
                        cur=cur,
                    )
                else:
                    ruleset = query_ruleset[0]

                for violation_name, violation_dict in ruleset_dict.get(
                    "violations", {}
                ).items():
                    query_violation = self.select_violation(
                        violation_name=violation_name,
                        ruleset_id=ruleset["ruleset_id"],
                        cur=cur,
                    )

                    if len(query_violation) >= 2:
                        raise Exception("Multiple rulesets found.")
                    elif len(query_violation) == 0:
                        violation = self.insert_violation(
                            violation_name=violation_name,
                            ruleset_id=ruleset["ruleset_id"],
                            category=violation_dict.get("category", "potential"),
                            labels=violation_dict.get("labels", []),
                            cur=cur,
                        )
                    else:
                        violation = query_violation[0]

                    for incident in violation_dict.get("incidents", []):
                        cur.execute(
                            """INSERT INTO incidents_temp(violation_id, application_id, incident_uri, incident_snip, incident_line, incident_variables)
              VALUES (%s, %s, %s, %s, %s, %s);""",
                            (
                                violation["violation_id"],
                                application["application_id"],
                                incident.get("uri", ""),
                                incident.get("codeSnip", ""),
                                incident.get("lineNumber", 0),
                                json.dumps(incident.get("variables", {})),
                            ),
                        )

            # incidents_temp - incidents
            cur.execute(
                """WITH filtered_incidents_temp AS (
    SELECT * FROM incidents_temp WHERE application_id = %s
),
filtered_incidents AS (
    SELECT * FROM incidents WHERE application_id = %s
)
SELECT fit.incident_id AS incidents_temp_id, fi.incident_id AS incidents_id, fit.violation_id, fit.application_id, fit.incident_uri, fit.incident_snip, fit.incident_line, fit.incident_variables
FROM filtered_incidents_temp fit
LEFT JOIN filtered_incidents fi ON fit.violation_id = fi.violation_id
                                AND fit.incident_uri = fi.incident_uri
                                AND fit.incident_snip = fi.incident_snip
                                AND fit.incident_line = fi.incident_line
                                AND fit.incident_variables = fi.incident_variables
WHERE fi.incident_id IS NULL;""",
                (
                    application["application_id"],
                    application["application_id"],
                ),
            )

            new_incidents = cur.fetchall()
            number_new_incidents = len(new_incidents)

            self.conn.autocommit = False
            for ni in new_incidents:
                self.insert_incident(
                    ni["violation_id"],
                    ni["application_id"],
                    ni["incident_uri"],
                    ni["incident_snip"],
                    ni["incident_line"],
                    ni["incident_variables"],
                    None,
                    cur,
                )
            self.conn.commit()
            cur.fetchall()
            self.conn.autocommit = True

            # incidents `intersect` incidents_temp
            cur.execute(
                """-- incidents `intersect` incidents_temp with application_id match first
WITH filtered_incidents AS (
    SELECT * FROM incidents WHERE application_id = %s
),
filtered_incidents_temp AS (
    SELECT * FROM incidents_temp WHERE application_id = %s
)
SELECT fi.incident_id AS incidents_id, fit.incident_id AS incidents_temp_id, fi.violation_id, fi.application_id, fi.incident_uri, fi.incident_snip, fi.incident_line, fi.incident_variables
FROM filtered_incidents fi
JOIN filtered_incidents_temp fit ON fi.violation_id = fit.violation_id
                                  AND fi.incident_uri = fit.incident_uri
                                  AND fi.incident_snip = fit.incident_snip
                                  AND fi.incident_line = fit.incident_line
                                  AND fi.incident_variables = fit.incident_variables;
""",
                (
                    application["application_id"],
                    application["application_id"],
                ),
            )

            unsolved_incidents = cur.fetchall()
            number_unsolved_incidents = len(unsolved_incidents)

            # incidents - incidents_temp
            cur.execute(
                """WITH filtered_incidents AS (
    SELECT * FROM incidents WHERE application_id = %s
),
filtered_incidents_temp AS (
    SELECT * FROM incidents_temp WHERE application_id = %s
)
SELECT fi.incident_id AS incidents_id, fit.incident_id AS incidents_temp_id, fi.violation_id, fi.application_id, fi.incident_uri, fi.incident_snip, fi.incident_line, fi.incident_variables
FROM filtered_incidents fi
LEFT JOIN filtered_incidents_temp fit ON fi.violation_id = fit.violation_id
                                      AND fi.incident_uri = fit.incident_uri
                                      AND fi.incident_snip = fit.incident_snip
                                      AND fi.incident_line = fit.incident_line
                                      AND fi.incident_variables = fit.incident_variables
WHERE fit.incident_id IS NULL;""",
                (
                    application["application_id"],
                    application["application_id"],
                ),
            )

            solved_incidents = cur.fetchall()
            number_solved_incidents = len(solved_incidents)
            KAI_LOG.debug(f"# of solved inc: {len(solved_incidents)}")

            self.conn.autocommit = False
            for si in solved_incidents:
                file_path = os.path.join(
                    repo_path,
                    unquote(urlparse(si[4]).path).removeprefix("/tmp/source-code/"),
                )
                big_diff = repo.git.diff(old_commit, new_commit)

                try:
                    original_code = repo.git.show(f"{old_commit}:{file_path}")
                except Exception:
                    original_code = ""

                try:
                    updated_code = repo.git.show(f"{new_commit}:{file_path}")
                except Exception:
                    updated_code = ""

                # file_path = pathlib.Path(os.path.join(repo_path, unquote(urlparse(si[3]).path).removeprefix('/tmp/source-code'))).as_uri()
                small_diff = repo.git.diff(old_commit, new_commit, "--", file_path)

                sln = self.insert_accepted_solution(
                    app.generated_at,
                    big_diff,
                    small_diff,
                    original_code,
                    updated_code,
                    cur,
                )

                cur.execute(
                    "UPDATE incidents SET solution_id = %s WHERE incident_id = %s;",
                    (sln["solution_id"], si[0]),
                )

            self.conn.commit()
            self.conn.autocommit = True

            cur.execute("DROP TABLE IF EXISTS incidents_temp;")
            application = self.update_application(
                application["application_id"], app, cur
            )

        return number_new_incidents, number_unsolved_incidents, number_solved_incidents

    # Automatic vs manual solution acceptance

    def accept_solution_from_id(
        self,
        incident_id: int,
        solution_id: int | None,
    ):
        pass

    def accept_solution_from_diff():
        pass

    def load_store(self, path: str):
        # fetch the output.yaml files from the analysis_reports/initial directory

        basedir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(basedir)
        folder_path = os.path.join(parent_dir, path)

        if not os.path.exists(folder_path):
            KAI_LOG.error(f"Error: {folder_path} does not exist.")
            return None
        # check if the folder is empty
        if not os.listdir(folder_path):
            KAI_LOG.error(f"Error: {folder_path} is empty.")
            return None
        apps = os.listdir(folder_path)
        KAI_LOG.info(f"Loading incident store with applications: {apps}\n")

        for app in apps:

            # if app is a directory then check if there is a folder called initial
            KAI_LOG.info(f"Loading application {app}\n")
            app_path = os.path.join(folder_path, app)
            if os.path.isdir(app_path):
                initial_folder = os.path.join(app_path, "initial")
                if not os.path.exists(initial_folder):
                    KAI_LOG.error(f"Error: {initial_folder} does not exist.")
                    return None
                # check if the folder is empty
                if not os.listdir(initial_folder):
                    KAI_LOG.error(
                        f"Error: No analysis report found in {initial_folder}."
                    )
                    return None
                report_path = os.path.join(initial_folder, "output.yaml")

                repo_path = self.get_repo_path(app)
                repo = Repo(repo_path)
                app_v = self.get_app_variables(folder_path, app)
                initial_branch = app_v["initial_branch"]
                repo.git.checkout(initial_branch)
                commit = repo.head.commit

                app_initial = Application(
                    application_id=None,
                    application_name=app,
                    repo_uri_origin=repo.remotes.origin.url,
                    repo_uri_local=repo_path,
                    current_branch=initial_branch,
                    current_commit=commit.hexsha,
                    generated_at=datetime.datetime.now(),
                )

                KAI_LOG.info(f"Loading application {app}\n")

                self.insert_and_update_from_report(app_initial, Report(report_path))
                KAI_LOG.info(f"Loaded application - initial {app}\n")

                # input(f"After inserting initial for {app}...")

                solved_folder = os.path.join(app_path, "solved")
                if not os.path.exists(solved_folder):
                    KAI_LOG.error(f"Error: {solved_folder} does not exist.")
                    return None
                # check if the folder is empty
                if not os.listdir(solved_folder):
                    KAI_LOG.error(
                        f"Error: No analysis report found in {solved_folder}."
                    )
                    return None
                report_path = os.path.join(solved_folder, "output.yaml")
                solved_branch = self.get_app_variables(folder_path, app)[
                    "solved_branch"
                ]
                repo.git.checkout(solved_branch)
                commit = repo.head.commit
                app_solved = Application(
                    application_id=None,
                    application_name=app,
                    repo_uri_origin=repo.remotes.origin.url,
                    repo_uri_local=repo_path,
                    current_branch=solved_branch,
                    current_commit=commit.hexsha,
                    generated_at=datetime.datetime.now(),
                )
                self.insert_and_update_from_report(app_solved, Report(report_path))

                KAI_LOG.info(f"Loaded application - solved {app}\n")

    def get_repo_path(self, app_name):
        """
        Get the repo path
        """

        # TODO:  This mapping data should be moved out of the code, consider moving to a config file
        mapping = {
            "eap-coolstore-monolith": "samples/sample_repos/eap-coolstore-monolith",
            "ticket-monster": "samples/sample_repos/ticket-monster",
            "kitchensink": "samples/sample_repos/kitchensink",
            "helloworld-mdb": "samples/sample_repos/helloworld-mdb",
            "bmt": "samples/sample_repos/bmt",
            "cmt": "samples/sample_repos/cmt",
            "ejb-remote": "samples/sample_repos/ejb-remote",
            "ejb-security": "samples/sample_repos/ejb-security",
            "tasks-qute": "samples/sample_repos/tasks-qute",
            "greeter": "samples/sample_repos/greeter",
        }

        basedir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(basedir)
        path = mapping.get(app_name, None)
        return os.path.join(parent_dir, path)

    def get_app_variables(self, path: str, app_name: str):

        if not os.path.exists(path):
            KAI_LOG.error(
                f"Error: {app_name} does not exist in the analysis_reports directory."
            )
            return None

        # Path to the app.yaml file
        app_yaml_path = os.path.join(path, app_name, "app.yaml")
        # Check if app.yaml exists for the specified app
        if not os.path.exists(app_yaml_path):
            KAI_LOG.error(f"Error: app.yaml does not exist for {app_name}.")
            return None

        # Load contents of app.yaml
        with open(app_yaml_path, "r") as app_yaml_file:
            app_data: dict = yaml.safe_load(app_yaml_file)

        return app_data


def main():
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument(
        "--config_filepath",
        type=str,
        default="database.ini",
        help="Path to the config file.",
    )
    parser.add_argument(
        "--config_section",
        type=str,
        default="postgresql",
        help="Config section in the config file.",
    )
    parser.add_argument(
        "--drop_tables", type=str, default="False", help="Whether to drop tables."
    )
    parser.add_argument(
        "--analysis_dir_path",
        type=str,
        default="samples/analysis_reports",
        help="path to analysis reports folder",
    )
    args = parser.parse_args()

    psqlis = PSQLIncidentStore(
        config_filepath=args.config_filepath,
        config_section=args.config_section,
        emb_provider=EmbeddingNone(),
    )
    path = args.analysis_dir_path
    if args.drop_tables:
        psqlis.delete_store()
    psqlis.load_store(path)


if __name__ == "__main__":
    main()
