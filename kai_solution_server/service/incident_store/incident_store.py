import argparse
import datetime
import logging
import os
from dataclasses import dataclass
from typing import Any, Optional, TypeVar, cast
from urllib.parse import unquote, urlparse

import yaml
from git import Repo
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from kai.analyzer_types import Report, filter_incident_vars
from kai.constants import PATH_GIT_ROOT, PATH_LOCAL_REPO
from kai.kai_config import KaiConfig
from kai.logging.logging import get_logger
from kai_solution_server.service.incident_store.backend import (
    IncidentStoreBackend,
    incident_store_backend_factory,
)
from kai_solution_server.service.incident_store.sql_types import (
    SQLAcceptedSolution,
    SQLApplication,
    SQLBase,
    SQLIncident,
    SQLRuleset,
    SQLUnmodifiedReport,
    SQLViolation,
)
from kai_solution_server.service.llm_interfacing.model_provider import ModelProvider
from kai_solution_server.service.solution_handling.detection import (
    SolutionDetectionAlgorithm,
    SolutionDetectorContext,
    solution_detection_factory,
)
from kai_solution_server.service.solution_handling.production import (
    SolutionProducer,
    solution_producer_factory,
)
from kai_solution_server.service.solution_handling.solution_types import Solution

KAI_LOG = get_logger(__name__)

T = TypeVar("T")


def deep_sort(obj: T) -> T:
    if isinstance(obj, dict):
        return cast(T, {k: deep_sort(v) for k, v in sorted(obj.items())})
    if isinstance(obj, list):
        return cast(T, sorted(deep_sort(x) for x in obj))
    return obj


def __get_repo_path(app_name: str) -> str:
    """
    Get the repo path
    """
    return os.path.join(PATH_LOCAL_REPO, app_name)


def __get_app_variables(path: str, app_name: str) -> dict[str, Any] | None:
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
        app_data: dict[str, Any] = yaml.safe_load(app_yaml_file)

    return app_data


# NOTE: Once we integrate with Konveyor, this most likely will not be necessary
def load_reports_from_directory(store: "IncidentStore", path: str) -> None:
    basedir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(basedir)
    folder_path = os.path.join(parent_dir, path)

    if not os.path.exists(folder_path):
        KAI_LOG.error(f"Error: {folder_path} does not exist.")
        return None
    if not os.listdir(folder_path):
        KAI_LOG.error(f"Error: {folder_path} is empty.")
        return None

    apps = os.listdir(folder_path)
    KAI_LOG.info(f"Loading incident store with applications: {apps}\n")

    for app in apps:
        # if app is a directory then check if there is a folder called initial
        KAI_LOG.info(f"Loading application {app}\n")
        app_path = os.path.join(folder_path, app)

        if not os.path.isdir(app_path):
            continue

        initial_folder = os.path.join(app_path, "initial")
        if not os.path.exists(initial_folder):
            KAI_LOG.error(f"Error: {initial_folder} does not exist.")
            return None

        # Check if the `initial` folder is empty
        if not os.listdir(initial_folder):
            KAI_LOG.error(f"Error: No analysis report found in {initial_folder}.")
            return None

        report_path = os.path.join(initial_folder, "output.yaml")

        repo_path = __get_repo_path(app)
        repo = Repo(repo_path)
        app_v = __get_app_variables(folder_path, app)
        if app_v is None:
            return None
        initial_branch = app_v["initial_branch"]
        repo.git.checkout(initial_branch)
        commit = repo.head.commit

        app_initial = Application(
            application_name=app,
            repo_uri_origin=repo.remotes.origin.url,
            repo_uri_local=repo_path,
            current_branch=initial_branch,
            current_commit=commit.hexsha,
            generated_at=datetime.datetime.now(),
        )

        store.load_report(app_initial, Report.load_report_from_file(report_path))
        KAI_LOG.info(f"Loaded application - initial {app}\n")

        solved_folder = os.path.join(app_path, "solved")

        if not os.path.exists(solved_folder):
            KAI_LOG.error(f"Error: {solved_folder} does not exist.")
            return None

        if not os.listdir(solved_folder):
            KAI_LOG.error(f"Error: No analysis report found in {solved_folder}.")
            return None

        report_path = os.path.join(solved_folder, "output.yaml")
        app_vars = __get_app_variables(folder_path, app)
        if app_vars is None:
            return None
        solved_branch = app_vars["solved_branch"]

        repo.git.checkout(solved_branch)
        commit = repo.head.commit
        app_solved = Application(
            application_name=app,
            repo_uri_origin=repo.remotes.origin.url,
            repo_uri_local=repo_path,
            current_branch=solved_branch,
            current_commit=commit.hexsha,
            generated_at=datetime.datetime.now(),
        )
        store.load_report(app_solved, Report.load_report_from_file(report_path))

        KAI_LOG.info(f"Loaded application - solved {app}\n")


# NOTE: This application object is more like metadata than anything.
@dataclass
class Application:
    application_name: str
    repo_uri_origin: str
    repo_uri_local: str
    current_branch: str
    current_commit: str
    generated_at: datetime.datetime
    path: str = "."


class IncidentStore:
    def __init__(
        self,
        backend: IncidentStoreBackend,
        solution_detector: SolutionDetectionAlgorithm,
        solution_producer: SolutionProducer,
    ):
        self.backend = backend
        self.engine = self.backend.create_engine()

        self.solution_detector = solution_detector
        self.solution_producer = solution_producer

        self.create_tables()  # This is a no-op if the tables already exist

    def load_report(self, app: Application, report: Report) -> tuple[int, int, int]:
        """
        Load incidents from a report and given application object. Returns a
        tuple containing (# of new incidents, # of unsolved incidents, # of
        solved incidents) in that order.


        TODO: Only does stuff within the same application. Maybe fixed?
        """

        # NEW: Store whole report in table
        # - if we get the same report again, we should skip adding it. Have some identifier
        # - But should still check incidents.

        # - have two tables `unsolved_incidents` and `solved_incidents`

        # Iterate through all incidents in the report
        # - change so theres an identified like "commit application ruleset violation"

        repo = Repo(unquote(urlparse(app.repo_uri_local).path))
        old_commit: str
        new_commit = app.current_commit
        report_incidents: list[SQLIncident] = []

        with Session(self.engine) as session:
            select_report_stmt = select(SQLUnmodifiedReport).where(
                SQLUnmodifiedReport.report_id == report.report_id
            )

            if session.scalars(select_report_stmt).first() is not None:
                KAI_LOG.info(f"Report {report.report_id} already exists")
                return (0, 0, 0)

            select_application_stmt = select(SQLApplication).where(
                SQLApplication.application_name == app.application_name
            )

            application = session.scalars(select_application_stmt).first()

            if application is None:
                application = SQLApplication(
                    application_name=app.application_name,
                    repo_uri_origin=app.repo_uri_origin,
                    repo_uri_local=app.repo_uri_local,
                    current_branch=app.current_branch,
                    current_commit=app.current_commit,
                    generated_at=app.generated_at,
                    path=app.path,
                )
                session.add(application)
                session.commit()

            # TODO: Determine if we want to have this check
            # if application.generated_at >= app.generated_at:
            #     return 0, 0, 0

            old_commit = application.current_commit

            for ruleset_name, ruleset_obj in report.rulesets.items():
                if ruleset_obj is None:
                    continue

                ruleset_obj.model_dump_json()

                select_ruleset_stmt = select(SQLRuleset).where(
                    SQLRuleset.ruleset_name == ruleset_name
                )

                ruleset = session.scalars(select_ruleset_stmt).first()

                if ruleset is None:
                    ruleset = SQLRuleset(
                        ruleset_name=ruleset_name,
                        tags=ruleset_obj.tags,
                    )
                    session.add(ruleset)
                    session.commit()

                for violation_name, violation_obj in ruleset_obj.violations.items():
                    if violation_obj is None:
                        continue

                    select_violation_stmt = (
                        select(SQLViolation)
                        .where(SQLViolation.violation_name == violation_name)
                        .where(SQLViolation.ruleset_name == ruleset.ruleset_name)
                    )

                    violation = session.scalars(select_violation_stmt).first()

                    if violation is None:
                        violation = SQLViolation(
                            violation_name=violation_name,
                            ruleset_name=ruleset.ruleset_name,
                            category=violation_obj.category,
                            labels=violation_obj.labels,
                        )
                        session.add(violation)
                        session.commit()

                    for incident in violation_obj.incidents:
                        filtered_vars = filter_incident_vars(incident.variables)
                        report_incidents.append(
                            SQLIncident(
                                violation_name=violation.violation_name,
                                ruleset_name=ruleset.ruleset_name,
                                application_name=application.application_name,
                                application_path=application.path,
                                incident_uri=incident.uri,
                                incident_snip=incident.code_snip,
                                incident_line=incident.line_number,
                                incident_variables=deep_sort(filtered_vars),
                                incident_message=incident.message,
                            )
                        )

            solution_detector_ctx = SolutionDetectorContext(
                old_incidents=application.incidents,
                new_incidents=report_incidents,
                repo=repo,
                old_commit=old_commit,
                new_commit=new_commit,
                app_path=application.path,
            )

            categorized_incidents = self.solution_detector(solution_detector_ctx)

            # create entries if not exists
            #           old
            #         | NO     | YES
            # --------|--------+-----------------------------
            # new NO  | -      | update (SOLVED, embeddings)
            #     YES | insert | update (line number, etc...)

            # Add new incidents

            session.add_all(categorized_incidents.new)
            session.commit()

            KAI_LOG.debug(
                f"Number of solved incidents: {len(categorized_incidents.solved)}"
            )

            # Update solved incidents with their respective solutions

            for solved_incident in categorized_incidents.solved:
                solution = self.solution_producer.produce_one(
                    solved_incident, repo, old_commit, new_commit
                )
                solved_incident.solution = SQLAcceptedSolution(
                    solution=solution,
                )

            session.commit()

            application.repo_uri_origin = app.repo_uri_origin
            application.repo_uri_local = app.repo_uri_local
            application.current_branch = app.current_branch
            application.current_commit = app.current_commit
            application.generated_at = app.generated_at

            session.commit()

            report_dict = {
                k: v.model_dump(mode="json") for k, v in report.rulesets.items()
            }
            unmodified_report = SQLUnmodifiedReport(
                application_name=app.application_name,
                report_id=report.report_id,
                generated_at=app.generated_at,
                report=report_dict,
            )

            # Upsert the unmodified report
            session.merge(unmodified_report)
            session.commit()

        return (
            len(categorized_incidents.new),
            len(categorized_incidents.unsolved),
            len(categorized_incidents.solved),
        )

    def create_tables(self) -> None:
        """
        Create tables in the incident store.
        """
        SQLBase.metadata.create_all(self.engine)

    def delete_store(self) -> None:
        """
        Clears all data within the incident store. Non-reversible!
        """
        SQLBase.metadata.drop_all(self.engine)
        self.create_tables()

    def find_solutions(
        self,
        ruleset_name: str,
        violation_name: str,
        incident_variables: dict[str, Any],
        incident_snip: Optional[str] = None,
    ) -> list[Solution]:
        """
        Returns a list of solutions for the given incident. Exact matches only.
        """
        incident_variables = deep_sort(filter_incident_vars(incident_variables))

        if incident_snip is None:
            incident_snip = ""

        with Session(self.engine) as session:
            select_violation_stmt = (
                select(SQLViolation)
                .where(SQLViolation.violation_name == violation_name)
                .where(SQLViolation.ruleset_name == ruleset_name)
            )

            violation = session.scalars(select_violation_stmt).first()

            if violation is None:
                return []

            select_incidents_with_solutions_stmt = (
                select(SQLIncident)
                .where(SQLIncident.violation_name == violation.violation_name)
                .where(SQLIncident.ruleset_name == violation.ruleset_name)
                .where(SQLIncident.solution_id.isnot(None))
                .where(self.backend.json_exactly_equal(incident_variables))
            )

            result: list[Solution] = []
            for incident in session.scalars(select_incidents_with_solutions_stmt).all():
                select_accepted_solution_stmt = select(SQLAcceptedSolution).where(
                    SQLAcceptedSolution.solution_id == incident.solution_id
                )

                accepted_solution = session.scalars(
                    select_accepted_solution_stmt
                ).first()

                if accepted_solution is not None:
                    result.append(accepted_solution.solution)
            return result

    def post_process(self, limit: int = 5) -> None:
        """Runs post_process function of producer for all applicable solutions
        It can take significant amount of time (~50-60 secs per solution) to run this for all solutions at once.
        A positive limit value will limit the number of solutions processed.

        Args:
            limit (int, optional): Max number of solutions to pick. -ve value picks "all". Defaults to 5.
        """
        page_size = 100
        page = 0
        processed_count = 0

        # FIXME: Basically if limit is less than zero, then we treat it as
        # "there is no limit". There is no maximum integer value in Python. Mypy
        # complains here because we're assigning a float to an int. A better way
        # to do this would be to modify the while loop below here.
        limit = float("inf") if limit < 0 else limit  # type: ignore[assignment]
        KAI_LOG.debug(f"Running post_process with limit {limit}")
        with Session(self.engine) as session:
            while processed_count < limit:
                select_solutions_without_summary_stmt = (
                    select(SQLAcceptedSolution)
                    .limit(page_size)
                    .offset(page * page_size)
                )

                page += 1

                solutions = session.scalars(select_solutions_without_summary_stmt).all()

                if len(solutions) < 1:
                    break

                for original_solution in solutions:
                    original_sol = original_solution.solution.model_copy()
                    select_incidents_for_solution_stmt = select(SQLIncident).where(
                        SQLIncident.solution_id == original_solution.solution_id
                    )
                    related_incident = session.scalars(
                        select_incidents_for_solution_stmt
                    ).first()
                    if related_incident is None:
                        KAI_LOG.debug(
                            f"No incident found for solution {original_solution.solution_id}"
                        )
                        continue
                    KAI_LOG.debug(
                        f"Running producer post_process for solution {original_solution.solution_id}"
                    )
                    try:
                        processed_solution = self.solution_producer.post_process_one(
                            related_incident, original_solution.solution
                        )
                        if original_sol.model_dump() == processed_solution.model_dump():
                            KAI_LOG.debug(
                                f"Skipping already processed solution {original_solution.solution_id}"
                            )
                        else:
                            # (pgaikwad): since we have a custom TypeDecorator on solution field
                            # we need to force set modified flag, this may be done better
                            flag_modified(original_solution, "solution")
                            processed_count += 1
                            KAI_LOG.debug(
                                f"Processed solution {original_solution.solution_id}"
                            )
                            session.commit()
                            if processed_count >= limit:
                                break
                    except Exception as e:
                        KAI_LOG.error(f"Error running post_process - {e}")
            else:
                KAI_LOG.debug(f"Processed {processed_count} solutions, limit {limit}")

    @staticmethod
    def incident_store_from_config(config: KaiConfig) -> "IncidentStore":
        model_provider = ModelProvider(config.models)

        KAI_LOG.info(f"Selected provider: {config.models.provider}")
        KAI_LOG.info(f"Selected model: {model_provider.model_id}")

        backend = incident_store_backend_factory(config.incident_store.args)

        solution_detector = solution_detection_factory(
            config.incident_store.solution_detectors
        )

        solution_producer = solution_producer_factory(
            config.incident_store.solution_producers, model_provider
        )

        return IncidentStore(
            backend=backend,
            solution_detector=solution_detector,
            solution_producer=solution_producer,
        )


def cmd(provider: str | None = None) -> None:
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument(
        "--config_filepath",
        type=str,
        default=None,
        required=True,
        help="Path to the config file.",
    )
    parser.add_argument(
        "--drop_tables", action="store_true", help="Whether to drop tables."
    )
    parser.add_argument(
        "--analysis_dir_path",
        type=str,
        default=os.path.join(
            PATH_GIT_ROOT, "kai_solution_server/samples/analysis_reports/"
        ),
        help="Path to analysis reports folder",
    )
    parser.add_argument(
        "--post_process",
        action="store_true",
        help="Whether to run producer post process",
    )
    parser.add_argument(
        "--post_process_limit",
        type=int,
        default=-1,
        help="Whether to run producer post process",
    )
    console_handler = logging.StreamHandler()
    KAI_LOG.addHandler(console_handler)
    KAI_LOG.setLevel("DEBUG")

    args = parser.parse_args()

    if args.config_filepath:
        config = KaiConfig.model_validate_filepath(args.config_filepath)
    else:
        config = KaiConfig()

    KAI_LOG.info(f"config: {config}")
    incident_store = IncidentStore.incident_store_from_config(config)

    if provider is not None and config.incident_store.args.provider != provider:
        raise Exception(f"This script only works with {provider} incident store.")

    incident_store = IncidentStore.incident_store_from_config(config)

    if args.drop_tables:
        incident_store.delete_store()

    if args.post_process:
        incident_store.post_process(limit=args.post_process_limit)
    else:
        load_reports_from_directory(incident_store, args.analysis_dir_path)


if __name__ == "__main__":
    cmd()
