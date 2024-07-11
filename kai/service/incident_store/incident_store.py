import argparse
import datetime
import enum
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, TypeVar
from urllib.parse import unquote, urlparse

import yaml
from git import Repo
from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    func,
    select,
)
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.types import JSON

from kai.constants import PATH_LOCAL_REPO
from kai.kai_logging import KAI_LOG
from kai.model_provider import ModelProvider
from kai.models.kai_config import (
    KaiConfig,
    KaiConfigIncidentStore,
    KaiConfigIncidentStoreProvider,
)
from kai.report import Report

# These prefixes are sometimes in front of the paths, strip them.
# Also strip leading slashes since os.path.join can't join two absolute paths
KNOWN_PREFIXES = (
    "/opt/input/source/",
    # trunk-ignore(bandit/B108)
    "/tmp/source-code/",
    "/addon/source/",
    "/",
)


# These are known unique variables that can be included by incidents
# They would prevent matches that we actually want, so we filter them
# before adding to the database or searching
FILTERED_INCIDENT_VARS = ("file", "package")


def remove_known_prefixes(path: str) -> str:
    for prefix in KNOWN_PREFIXES:
        if path.startswith(prefix):
            return path.removeprefix(prefix)
    return path


def filter_incident_vars(incident_vars: dict):
    for v in FILTERED_INCIDENT_VARS:
        incident_vars.pop(v, None)
    return incident_vars


T = TypeVar("T")


def deep_sort(obj: T) -> T:
    if isinstance(obj, dict):
        return {k: deep_sort(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        return sorted(deep_sort(x) for x in obj)
    return obj


def __get_repo_path(app_name):
    """
    Get the repo path
    """
    return os.path.join(PATH_LOCAL_REPO, app_name)


def __get_app_variables(path: str, app_name: str):
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


# NOTE: Once we integrate with Konveyor, this most likely will not be necessary
def load_reports_from_directory(store: "IncidentStore", path: str):
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
        solved_branch = __get_app_variables(folder_path, app)["solved_branch"]

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


@dataclass
class Application:
    application_name: str
    repo_uri_origin: str
    repo_uri_local: str
    current_branch: str
    current_commit: str
    generated_at: datetime.datetime


# NOTE(@JonahSussman): Should we include the incident that this solution is for
# inside the class?
@dataclass
class Solution:
    uri: str
    file_diff: str
    repo_diff: str
    original_code: Optional[str] = None
    updated_code: Optional[str] = None


class SQLBase(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON()
        .with_variant(postgresql.JSONB(), "postgresql")
        .with_variant(sqlite.JSON(), "sqlite"),
        list[str]: JSON()
        .with_variant(postgresql.JSONB(), "postgresql")
        .with_variant(sqlite.JSON(), "sqlite"),
    }


class SQLUnmodifiedReport(SQLBase):
    __tablename__ = "unmodified_reports"

    application_name: Mapped[str] = mapped_column(primary_key=True)
    report_id: Mapped[str] = mapped_column(primary_key=True)

    generated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    report: Mapped[dict[str, Any]]


class ViolationCategory(enum.Enum):
    potential = "potential"
    optional = "optional"
    mandatory = "mandatory"


class SQLApplication(SQLBase):
    __tablename__ = "applications"

    application_name: Mapped[str] = mapped_column(primary_key=True)

    repo_uri_origin: Mapped[str]
    repo_uri_local: Mapped[str]
    current_branch: Mapped[str]
    current_commit: Mapped[str]
    generated_at: Mapped[datetime.datetime]

    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="application", cascade="all, delete-orphan"
    )


class SQLRuleset(SQLBase):
    __tablename__ = "rulesets"

    ruleset_name: Mapped[str] = mapped_column(primary_key=True)

    tags: Mapped[list[str]]

    violations: Mapped[list["SQLViolation"]] = relationship(
        back_populates="ruleset", cascade="all, delete-orphan"
    )


class SQLViolation(SQLBase):
    __tablename__ = "violations"

    violation_name: Mapped[str] = mapped_column(primary_key=True)
    ruleset_name: Mapped[int] = mapped_column(
        ForeignKey("rulesets.ruleset_name"), primary_key=True
    )

    category: Mapped[ViolationCategory]
    labels: Mapped[list[str]]

    ruleset: Mapped[SQLRuleset] = relationship(back_populates="violations")
    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="violation", cascade="all, delete-orphan"
    )


class SQLAcceptedSolution(SQLBase):
    __tablename__ = "accepted_solutions"

    solution_id: Mapped[int] = mapped_column(primary_key=True)

    generated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    solution_big_diff: Mapped[str]
    solution_small_diff: Mapped[str]
    solution_original_code: Mapped[str]
    solution_updated_code: Mapped[str]

    llm_summary: Mapped[Optional[str]]

    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="solution", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"SQLAcceptedSolution(solution_id={self.solution_id}, generated_at={self.generated_at}, solution_big_diff={self.solution_big_diff:.10}, solution_small_diff={self.solution_small_diff:.10}, solution_original_code={self.solution_original_code:.10}, solution_updated_code={self.solution_updated_code:.10})"


class SQLIncident(SQLBase):
    __tablename__ = "incidents"

    incident_id: Mapped[int] = mapped_column(primary_key=True)

    violation_name = Column(String)
    ruleset_name = Column(String)
    application_name: Mapped[str] = mapped_column(
        ForeignKey("applications.application_name")
    )
    incident_uri: Mapped[str]
    incident_snip: Mapped[str]
    incident_line: Mapped[int]
    incident_variables: Mapped[dict[str, Any]]
    solution_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("accepted_solutions.solution_id")
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [violation_name, ruleset_name],
            [SQLViolation.violation_name, SQLViolation.ruleset_name],
        ),
        {},
    )

    violation: Mapped[SQLViolation] = relationship(back_populates="incidents")
    application: Mapped[SQLApplication] = relationship(back_populates="incidents")
    solution: Mapped[SQLAcceptedSolution] = relationship(back_populates="incidents")

    def __repr__(self) -> str:
        return f"SQLIncident(violation_name={self.violation_name}, ruleset_name={self.ruleset_name}, application_name={self.application_name}, incident_uri={self.incident_uri}, incident_snip={self.incident_snip:.10}, incident_line={self.incident_line}, incident_variables={self.incident_variables}, solution_id={self.solution_id})"


class IncidentStore(ABC):
    """
    Responsible for 3 main things:
    - Incident/Solution storage
    - Solution detection
    - Solution generation
    """

    engine: Engine
    model_provider: ModelProvider

    @staticmethod
    def from_config(config: KaiConfigIncidentStore, model_provider: ModelProvider):
        """
        Factory method to produce whichever incident store is needed.
        """

        # TODO: Come up with some sort of "solution generator strategy" so we
        # don't blow up our llm API usage. Lazy, immediate, other etc...

        if config.provider == "postgresql":
            from kai.service.incident_store.psql import PSQLIncidentStore

            return PSQLIncidentStore(config.args, model_provider)
        elif config.provider == "sqlite":
            from kai.service.incident_store.sqlite import SQLiteIncidentStore

            return SQLiteIncidentStore(config.args, model_provider)
        else:
            raise ValueError(
                f"Unsupported provider: {config.provider}\ntype: {type(config.provider)}\nlmao: {KaiConfigIncidentStoreProvider.POSTGRESQL}"
            )

    def load_report(self, app: Application, report: Report) -> tuple[int, int, int]:
        """
        Load incidents from a report and given application object. Returns a
        tuple containing (# of new incidents, # of unsolved incidents, # of
        solved incidents) in that order.

        NOTE: This application object is more like metadata than anything.
        """

        # FIXME: Only does stuff within the same application. Maybe fixed?

        # NEW: Store whole report in table
        # - if we get the same report again, we should skip adding it. Have some identifier
        # - But should still check incidents.

        # - have two tables `unsolved_incidents` and `solved_incidents`

        # Iterate through all incidents in the report
        # - change so theres an identified like "commit application ruleset violation"

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

        with Session(self.engine) as session:
            incidents_temp: list[SQLIncident] = []

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
                )
                session.add(application)
                session.commit()

            # TODO: Determine if we want to have this check
            # if application.generated_at >= app.generated_at:
            #     return 0, 0, 0

            old_commit = application.current_commit

            report_dict = dict(report)

            for ruleset_name, ruleset_dict in report_dict.items():
                select_ruleset_stmt = select(SQLRuleset).where(
                    SQLRuleset.ruleset_name == ruleset_name
                )

                ruleset = session.scalars(select_ruleset_stmt).first()

                if ruleset is None:
                    ruleset = SQLRuleset(
                        ruleset_name=ruleset_name,
                        tags=ruleset_dict.get("tags", []),
                    )
                    session.add(ruleset)
                    session.commit()

                for violation_name, violation_dict in ruleset_dict.get(
                    "violations", {}
                ).items():
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
                            category=violation_dict.get("category", "potential"),
                            labels=violation_dict.get("labels", []),
                        )
                        session.add(violation)
                        session.commit()

                    for incident in violation_dict.get("incidents", []):
                        incidents_temp.append(
                            SQLIncident(
                                violation_name=violation.violation_name,
                                ruleset_name=ruleset.ruleset_name,
                                application_name=application.application_name,
                                incident_uri=incident.get("uri", ""),
                                incident_snip=incident.get("codeSnip", ""),
                                incident_line=incident.get("lineNumber", 0),
                                incident_variables=deep_sort(
                                    incident.get("variables", {})
                                ),
                            )
                        )

            # incidents_temp - incidents
            new_incidents = set(incidents_temp) - set(application.incidents)
            number_new_incidents = len(new_incidents)

            for new_incident in new_incidents:
                session.add(new_incident)

            session.commit()

            # incidents `intersect` incidents_temp
            unsolved_incidents = set(application.incidents).intersection(incidents_temp)
            number_unsolved_incidents = len(unsolved_incidents)

            # incidents - incidents_temp
            solved_incidents = set(application.incidents) - set(incidents_temp)
            number_solved_incidents = len(solved_incidents)
            KAI_LOG.debug(f"Number of solved incidents: {len(solved_incidents)}")
            # KAI_LOG.debug(f"{solved_incidents=}")

            for solved_incident in solved_incidents:
                file_path = os.path.join(
                    repo_path,
                    # NOTE: When retrieving uris from the report, some of them
                    # had "/tmp/source-code/" as their root path. Unsure where
                    # it originates from.
                    unquote(urlparse(solved_incident.incident_uri).path).removeprefix(
                        "/tmp/source-code/"  # trunk-ignore(bandit/B108)
                    ),
                )

                # NOTE: The `big_diff` functionality is currently disabled

                # big_diff: str = repo.git.diff(old_commit, new_commit).encode('utf-8', errors="ignore").decode()
                big_diff = ""

                # TODO: Some of the sample repos have invalid utf-8 characters,
                # thus the encode-then-decode hack. Not very performant, there's
                # probably a better way to handle this.

                try:
                    original_code = (
                        repo.git.show(f"{old_commit}:{file_path}")
                        .encode("utf-8", errors="ignore")
                        .decode()
                    )
                except Exception:
                    original_code = ""

                try:
                    updated_code = (
                        repo.git.show(f"{new_commit}:{file_path}")
                        .encode("utf-8", errors="ignore")
                        .decode()
                    )
                except Exception:
                    updated_code = ""

                small_diff = (
                    repo.git.diff(old_commit, new_commit, "--", file_path)
                    .encode("utf-8", errors="ignore")
                    .decode()
                )

                # TODO: Strings must be utf-8 encodable, so I'm removing the `big_diff` functionality for now
                solved_incident.solution = SQLAcceptedSolution(
                    generated_at=app.generated_at,
                    solution_big_diff=big_diff,
                    solution_small_diff=small_diff,
                    solution_original_code=original_code,
                    solution_updated_code=updated_code,
                )

                session.commit()

            application.repo_uri_origin = app.repo_uri_origin
            application.repo_uri_local = app.repo_uri_local
            application.current_branch = app.current_branch
            application.current_commit = app.current_commit
            application.generated_at = app.generated_at

            session.commit()

            unmodified_report = SQLUnmodifiedReport(
                application_name=app.application_name,
                report_id=report.report_id,
                generated_at=app.generated_at,
                report=report_dict,
            )

            # Upsert the unmodified report
            session.merge(unmodified_report)
            session.commit()

        return number_new_incidents, number_unsolved_incidents, number_solved_incidents

    def create_tables(self):
        """
        Create tables in the incident store.
        """
        SQLBase.metadata.create_all(self.engine)

    def delete_store(self):
        """
        Clears all data within the incident store. Non-reversible!
        """
        SQLBase.metadata.drop_all(self.engine)
        self.create_tables()

    def find_solutions(
        self,
        ruleset_name: str,
        violation_name: str,
        incident_variables: dict,
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
                .where(self.json_exactly_equal(incident_variables))
            )

            result: list[Solution] = []
            for incident in session.execute(
                select_incidents_with_solutions_stmt
            ).scalars():
                select_accepted_solution_stmt = select(SQLAcceptedSolution).where(
                    SQLAcceptedSolution.solution_id == incident.solution_id
                )

                accepted_solution = session.scalars(
                    select_accepted_solution_stmt
                ).first()

                result.append(
                    Solution(
                        uri=incident.incident_uri,
                        file_diff=accepted_solution.solution_small_diff,
                        repo_diff=accepted_solution.solution_big_diff,
                    )
                )

            return result

    @abstractmethod
    def json_exactly_equal(self, json_dict: dict):
        """
        Each incident store must implement this method as JSON is handled
        slightly differently between SQLite and PostgreSQL.
        """
        pass


def cmd(provider: str = None):
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

    if provider is not None and config.incident_store.provider != provider:
        raise Exception(f"This script only works with {provider} incident store.")

    model_provider = ModelProvider(config.models)
    incident_store = IncidentStore.from_config(config.incident_store, model_provider)

    if args.drop_tables:
        incident_store.delete_store()

    load_reports_from_directory(incident_store, args.analysis_dir_path)


if __name__ == "__main__":
    cmd()
