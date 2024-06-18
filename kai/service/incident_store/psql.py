import argparse
import datetime
import json
import os
from functools import wraps
from inspect import signature
from urllib.parse import unquote, urlparse

import psycopg2
from git import Repo
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor, DictRow

from kai.constants import PATH_SQL
from kai.embedding_provider import EmbeddingNone
from kai.kai_logging import KAI_LOG
from kai.models.kai_config import KaiConfig, KaiConfigIncidentStorePostgreSQLArgs
from kai.report import Report
from kai.service.incident_store.incident_store import (
    Application,
    IncidentStore,
    Solution,
    filter_incident_vars,
    load_reports_from_directory,
    remove_known_prefixes,
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


# TODO(@JonahSussman): Migrate this to use an ORM
class PSQLIncidentStore(IncidentStore):
    def __init__(self, args: KaiConfigIncidentStorePostgreSQLArgs):
        self.emb_provider = EmbeddingNone()

        try:
            with psycopg2.connect(
                cursor_factory=DictCursor, **args.model_dump()
            ) as conn:
                KAI_LOG.info("Connected to the PostgreSQL server.")
                self.conn: connection = conn
                self.conn.autocommit = True

            self.create_tables()

        except (psycopg2.DatabaseError, Exception) as error:
            KAI_LOG.error(f"Error initializing PSQLIncidentStore: {error}")

    def create_tables(self):
        # TODO: Figure out portable way to install the pgvector extension.
        # Containerize? "CREATE EXTENSION IF NOT EXISTS vector;" Only works as
        # superuser

        # TODO: along with analyzer_types.py, we should really use something
        # like openapi to nail down the spec and autogenerate the types
        sql_create_tables = open(
            os.path.join(PATH_SQL, "create_tables.sql"), "r"
        ).read()
        sql_add_embedding = open(
            os.path.join(PATH_SQL, "add_embedding.sql"), "r"
        ).readlines()

        with self.conn.cursor() as cur:
            cur.execute(sql_create_tables)

            dim = self.emb_provider.get_dimension()
            for q in sql_add_embedding:
                cur.execute(q, (dim,))

    # Abstract base class implementations

    def delete_store(self):
        with self.conn.cursor() as cur:
            cur.execute(open(os.path.join(PATH_SQL, "drop_tables.sql"), "r").read())

        self.create_tables()

    def load_report(self, app: Application, report: Report) -> tuple[int, int, int]:
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

            query_app = self.select_application(None, app.application_name, cur)

            if len(query_app) >= 2:
                raise Exception(f"Multiple applications found for {app}.")
            elif len(query_app) == 0:
                application = self.insert_application(app, cur)
            else:
                application = query_app[0]

            old_commit = application["current_commit"]

            report_dict = dict(report)

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
                        incident_vars = filter_incident_vars(
                            incident.get("variables", {})
                        )
                        cur.execute(
                            """INSERT INTO incidents_temp(violation_id, application_id, incident_uri, incident_snip, incident_line, incident_variables)
              VALUES (%s, %s, %s, %s, %s, %s);""",
                            (
                                violation["violation_id"],
                                application["application_id"],
                                incident.get("uri", ""),
                                incident.get("codeSnip", ""),
                                incident.get("lineNumber", 0),
                                json.dumps(incident_vars),
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
                # NOTE: When retrieving uris from the report, some of them
                # had "/tmp/source-code/" as their root path. Unsure where
                # it originates from.
                file_path = remove_known_prefixes(unquote(urlparse(si[4]).path))
                # file_path = os.path.join(
                #     repo_path,
                #     in_repo_path,
                # )
                big_diff = repo.git.diff(old_commit, new_commit)

                try:
                    original_code = repo.git.show(f"{old_commit}:{file_path}")
                except Exception as e:
                    KAI_LOG.error(e)
                    original_code = ""

                try:
                    updated_code = repo.git.show(f"{new_commit}:{file_path}")
                except Exception as e:
                    KAI_LOG.error(e)
                    updated_code = ""

                # file_path = pathlib.Path(os.path.join(repo_path, unquote(urlparse(si[3]).path).removeprefix('/tmp/source-code'))).as_uri()
                small_diff = repo.git.diff(old_commit, new_commit, "--", file_path)
                KAI_LOG.debug(small_diff)

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

    def find_solutions(
        self,
        ruleset_name: str,
        violation_name: str,
        incident_variables: dict,
        incident_snip: str | None = None,
    ) -> list[Solution]:
        if incident_snip is None:
            incident_snip = ""

        with self.conn.cursor() as cur:
            incident_vars_str = json.dumps(filter_incident_vars(incident_variables))

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
                raise Exception(
                    f"More than one violation with name '{violation_name}' and ruleset name {ruleset_name}"
                )
            if len(violation_query) == 0:
                return []

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
                return []

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

            incidents_with_solutions = cur.fetchall()
            result: list[Solution] = []

            for incident in incidents_with_solutions:
                accepted_solution = self.select_accepted_solution(
                    incident["solution_id"], cur
                )

                result.append(
                    Solution(
                        uri=incident["incident_uri"],
                        file_diff=accepted_solution["solution_small_diff"],
                        repo_diff=accepted_solution["solution_big_diff"],
                    )
                )

            return result

    # Implementation specific to PSQLIncidentStore Methods

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
            (
                app.application_name,
                app.repo_uri_origin,
                app.repo_uri_local,
                app.current_branch,
                app.current_commit,
                app.generated_at,
            ),
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

        vars_str = json.dumps(filter_incident_vars(incident_variables))
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
        solution_original_code = (
            solution_original_code.encode("utf-8", "ignore")
            .decode("utf-8")
            .replace("\x00", "\uFFFD")
        )
        solution_updated_code = (
            solution_updated_code.encode("utf-8", "ignore")
            .decode("utf-8")
            .replace("\x00", "\uFFFD")
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

        incident_vars_str = json.dumps(filter_incident_vars(incident_vars))

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


def main():
    KAI_LOG.setLevel("debug".upper())

    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument(
        "--config_filepath",
        type=str,
        default="../../config.toml",
        help="Path to the config file.",
    )
    parser.add_argument(
        "--drop_tables", type=str, default="False", help="Whether to drop tables."
    )
    parser.add_argument(
        "--analysis_dir_path",
        type=str,
        default="../../samples/analysis_reports",
        help="Path to analysis reports folder",
    )

    args = parser.parse_args()

    config = KaiConfig.model_validate_filepath(args.config_filepath)

    if config.incident_store.provider != "postgresql":
        raise Exception("This script only works with PostgreSQL incident store.")

    incident_store = PSQLIncidentStore(config.incident_store.args)

    if args.drop_tables:
        incident_store.delete_store()

    load_reports_from_directory(incident_store, args.analysis_dir_path)


if __name__ == "__main__":
    main()
