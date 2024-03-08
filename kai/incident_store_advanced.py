import pathlib
import requests
import os
import random
from configparser import ConfigParser
from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import Any
from functools import wraps
from inspect import signature
import json
from urllib.parse import unquote, urlparse

from git import Repo

import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.extras import DictCursor, DictRow

import tiktoken

from InstructorEmbedding import INSTRUCTOR
import numpy
import torch

from report import Report


BASE_PATH = os.path.dirname(__file__)


class TrimStrategy(Enum):
  NONE       = 0
  TRIM_FRONT = 1
  TRIM_BACK  = 2
  TRIM_BOTH  = 3


def trim_list(toks: list, max_len: int, trim_strategy: TrimStrategy=TrimStrategy.TRIM_BOTH) -> list:
  if len(toks) > max_len:
    num_to_trim = len(toks)-max_len

    match trim_strategy:
      case TrimStrategy.NONE:
        raise Exception(f"With NONE trim strategy, too many tokens to embed ({len(toks)} > {max_len})!")
      case TrimStrategy.TRIM_FRONT:
        toks = toks[num_to_trim:]
      case TrimStrategy.TRIM_BACK:
        toks = toks[:-num_to_trim]
      case TrimStrategy.TRIM_BOTH:
        n_front = num_to_trim // 2
        n_back = num_to_trim - n_front

        toks = toks[n_front:-n_back]

  return toks


class EmbeddingProvider(ABC):
  @abstractmethod
  def get_embedding(self, inp: str) -> list | None:
    pass

  @abstractmethod
  def get_max_tokens(self) -> int:
    pass

  @abstractmethod
  def get_dimension(self) -> int:
    pass


class EmbeddingNone(EmbeddingProvider):
  def __init__(self):
    self.max_tokens = 128
    self.dimension  = 1


  def get_embedding(self, inp: str) -> list | None:
    return [0]


  def get_max_tokens(self) -> int:
    return self.max_tokens


  def get_dimension(self) -> int:
    return self.dimension


class EmbeddingOpenAI(EmbeddingProvider):
  """
  - link: https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
  """
  def __init__(self, openai_api_key: str, model: str='text-embedding-3-small') -> None:
    self.max_tokens = 8192
    self.dimension  = 1536

    self.openai_api_key = openai_api_key
    self.model          = 'text-embedding-3-small'


  def get_embedding(self, inp: str) -> list | None:
    enc  = tiktoken.encoding_for_model(self.model)
    toks = trim_list(enc.encode(inp), self.max_tokens)
    dec  = enc.decode(toks)

    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {self.openai_api_key}'
    }

    data = {
      'input': dec,
      'model': 'text-embedding-3-small'
    }

    response: requests.Response = requests.post(
      'https://api.openai.com/v1/embeddings',
      json=data, headers=headers
    )

    if response.status_code != 200:
      print('Error:', response.status_code, response.text)
      return None

    return response.json()['data'][0]['embedding']


  def get_max_tokens(self) -> int:
    return self.max_tokens


  def get_dimension(self) -> int:
    return self.dimension


class EmbeddingInstructor(EmbeddingProvider):
  """
  - link: https://huggingface.co/hkunlp/instructor-xl
  """
  def __init__(self, model: str='hkunlp/instructor-large') -> None:
    # It appears instructor cuts off all tokens after the 512 mark automatically

    self.max_tokens = 512 # TODO: find out
    self.dimension  = 768

    self.instructor = INSTRUCTOR(model)

  def get_embedding(self, inp: str) -> list | None:
    prompt = [['Represent the source code file for semantic similarity', inp]]
    toks = self.instructor.tokenize([inp])['input_ids'].tolist()[0]

    if len(toks) > self.max_tokens:
      print(f"Length of tokens is {len(toks)}. Truncating to {self.max_tokens}.")

    result: numpy.ndarray = self.instructor.encode(prompt).tolist()[0]
    return result

  def get_dimension(self) -> int:
    return self.dimension

  def get_max_tokens(self) -> int:
    return self.max_tokens


def embedding_playground(conn: connection, embp: EmbeddingProvider) -> None:
  table_name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(30))

  with conn.cursor() as cur:
    # I know, string interpolation in SQL. But this is a playground, not for
    # production!
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
      id SERIAL PRIMARY KEY,
      the_text TEXT,
      embedding vector(%s)
    )
    """, (embp.get_dimension(),))

    while True:
      try:
        inp = input("> ")
        emb = embp.get_embedding(inp)
        cur.execute(f"""
          INSERT INTO {table_name}(the_text, embedding)
          VALUES (%s, %s)
        """, (inp, str(emb),))

        cur.execute(f"SELECT the_text FROM {table_name} ORDER BY embedding <=> %s LIMIT 25;", (str(emb),))

        for row in cur.fetchall():
          print(row)
        print()

      except KeyboardInterrupt:
        cur.execute(f"DROP TABLE {table_name};")
        break


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
      application_id=row['application_id'],
      application_name=row['application_name'],
      repo_uri_origin=row['repo_uri_origin'],
      repo_uri_local=row['repo_uri_local'],
      current_branch=row['current_branch'],
      current_commit=row['current_commit'],
      generated_at=row['generated_at'],
    )


def supply_cursor_if_none(func):
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    sig = signature(func)
    bound_args = sig.bind(self, *args, **kwargs)
    bound_args.apply_defaults()

    if 'cur' not in bound_args.arguments or bound_args.arguments['cur'] is None:
      with self.conn.cursor() as cur:
        bound_args.arguments['cur'] = cur
        return func(*bound_args.args, **bound_args.kwargs)
    else:
      return func(*bound_args.args, **bound_args.kwargs)

  return wrapper


# TODO: Potentially create a Redis version of the incident store as well?

# TODO: Migrate this whole app to Django and use their native ORM stuff. Seems
# to be much cleaner than rolling it by hand - jsussman
class PSQLIncidentStore:
  def __init__(
    self, *, drop_tables: bool=False, config_filepath: str=None,
    config_section: str=None, config: dict=None,
    emb_provider: EmbeddingProvider=None,
  ):
    # Config parsing. Either comes from a dict or a .ini file
    cf_none = config_filepath is None
    cs_none = config_section is None
    cd_none = config is None

    if cf_none != cs_none:
      raise Exception("config_filepath and config_section must both be set if using .ini file.")
    if not (cf_none ^ cd_none):
      raise Exception("Must provide either config .ini or config dict.")

    if not cf_none:
      parser = ConfigParser()
      parser.read(config_filepath)

      config = {}
      if not parser.has_section(config_section):
        raise Exception(f"Section {config_section} not found in file {config_filepath}")

      for p in parser.items(config_section):
        config[p[0]] = p[1]


    # Embedding provider
    if emb_provider is None:
      raise Exception("emb_provider must not be None")

    self.emb_provider = emb_provider


    try:
      with psycopg2.connect(cursor_factory=DictCursor, **config) as conn:
        print('Connected to the PostgreSQL server.')
        self.conn: connection = conn
        self.conn.autocommit = True

      with self.conn.cursor() as cur:
        # TODO: Figure out portable way to install the pgvector extension.
        # Containerize? "CREATE EXTENSION IF NOT EXISTS vector;" Only works as
        # superuser

        # TODO: along with analyzer_types.py, we should really use something
        # like openapi to nail down the spec and autogenerate the types

        if drop_tables:
          cur.execute(open(f"{BASE_PATH}/data/sql/drop_tables.sql", "r").read())

        cur.execute(open(f"{BASE_PATH}/data/sql/create_tables.sql", "r").read())

        dim = self.emb_provider.get_dimension()
        for q in open(f"{BASE_PATH}/data/sql/add_embedding.sql", "r").readlines():
          cur.execute(q, (dim,))

    except (psycopg2.DatabaseError, Exception) as error:
      print(f"Error initializing PSQLIncidentStore: {error}")


  @supply_cursor_if_none
  def select_application(self, app_id: int, app_name: str = None, cur: DictCursor = None) -> list[DictRow]:
    if app_id is None and app_name is None:
      return []

    if app_id is not None:
      cur.execute(
        "SELECT * FROM applications WHERE application_id = %s;",
        (app_id,))
    elif app_name is not None:
      cur.execute(
        "SELECT * FROM applications WHERE application_name = %s;",
        (app_name,)
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
      app.as_tuple()[1:]
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def update_application(self, application_id: int, app: Application, cur: DictCursor = None) -> DictRow:
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
      (app.application_name, app.repo_uri_origin, app.repo_uri_local,
       app.current_branch, app.current_commit, app.generated_at, application_id)
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def select_ruleset(self, ruleset_id: int = None, ruleset_name: str = None, cur: DictCursor = None) -> list[DictRow]:
  # def select_ruleset(self, ruleset_id: int = None, ruleset_name: str = None, application_id: int = None, cur: DictCursor = None) -> list[DictRow]:
    if ruleset_id is not None:
      cur.execute(
        "SELECT * FROM rulesets WHERE ruleset_id = %s;",
        (ruleset_id,)
      )
    # elif ruleset_name is not None and application_id is not None:
    elif ruleset_name is not None:
      cur.execute(
        # "SELECT * FROM rulesets WHERE ruleset_name = %s AND application_id = %s;",
        "SELECT * FROM rulesets WHERE ruleset_name = %s;",
        # (ruleset_name, application_id,)
        (ruleset_name,)
      )
    else:
      raise Exception("At least one of ruleset_id or ruleset_name must be not None.")

    return cur.fetchall()


  @supply_cursor_if_none
  def insert_ruleset(self, ruleset_name: str, tags: list[str], cur: DictCursor = None) -> DictRow:
  # def insert_ruleset(self, ruleset_name: str, application_id: int, tags: list[str], cur: DictCursor = None) -> DictRow:
    cur.execute(
      # """INSERT INTO rulesets(ruleset_name, application_id, tags)
      """INSERT INTO rulesets(ruleset_name, tags)
      VALUES (%s, %s) RETURNING*;""",
      # VALUES (%s, %s, %s) RETURNING*;""",
      # (ruleset_name, application_id, json.dumps(tags))
      (ruleset_name, json.dumps(tags))
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def select_violation(self, violation_id: int = None, violation_name: str = None, ruleset_id: int = None, cur: DictCursor = None) -> list[DictRow]:
    if violation_id is not None:
      cur.execute(
        "SELECT * FROM violations WHERE violation_id = %s;",
        (violation_id,)
      )
    elif violation_name is not None and ruleset_id is not None:
      cur.execute(
        "SELECT * FROM violations WHERE violation_name = %s AND ruleset_id = %s;",
        (violation_name, ruleset_id,)
      )
    else:
      raise Exception("At least one of violation_id or (violation_name, ruleset_id) must be not None.")

    return cur.fetchall()


  @supply_cursor_if_none
  def insert_violation(self, violation_name: str, ruleset_id: int, category: str, labels: list[str], cur: DictCursor = None) -> DictRow:
    cur.execute(
      """INSERT INTO violations(violation_name, ruleset_id, category, labels)
      VALUES (%s, %s, %s, %s) RETURNING *;""",
      (violation_name, ruleset_id, category, json.dumps(sorted(labels)))
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def insert_incident(
    self, violation_id: int, application_id: int, incident_uri: str, incident_snip: str,
    incident_line: int, incident_variables: dict, solution_id: int = None,
    cur: DictCursor = None
  ) -> DictRow:
    # if isinstance(incident_variables, str):
    #   incident_variables = json.loads(incident_variables)
    # if not isinstance(incident_variables, list):
    #   raise Exception(f"incident_variables must be of type list. Got type '{type(incident_variables)}'")

    print(f"inserting {(violation_id, application_id, incident_uri, incident_line, json.dumps(incident_variables), solution_id,)}")

    cur.execute(
      """INSERT INTO incidents(violation_id, application_id, incident_uri, incident_snip, incident_line, incident_variables, solution_id, incident_snip_embedding)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
      (
        violation_id, application_id, incident_uri, incident_snip, incident_line,
        json.dumps(incident_variables), solution_id, str(self.emb_provider.get_embedding(incident_snip)))
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def insert_accepted_solution(
    self, generated_at: datetime.datetime, solution_big_diff: str,
    solution_small_diff: str, solution_original_code: str,
    solution_updated_code: str, cur: DictCursor = None
  ):
    print(f"insertint accepted sln {(generated_at)}")
    small_diff_embedding = str(self.emb_provider.get_embedding(solution_small_diff))
    original_code_embedding = str(self.emb_provider.get_embedding(solution_original_code))
    cur.execute(
      """INSERT INTO accepted_solutions(generated_at, solution_big_diff,
      solution_small_diff, solution_original_code, solution_updated_code,
      small_diff_embedding, original_code_embedding)
      VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
      (
        generated_at, solution_big_diff, solution_small_diff,
        solution_original_code, solution_updated_code, small_diff_embedding,
        original_code_embedding)
    )

    return cur.fetchone()


  @supply_cursor_if_none
  def select_accepted_solution(
    self, solution_id: int, cur: DictCursor = None
  ):
    cur.execute(
      "SELECT * FROM accepted_solutions WHERE solution_id = %s;",
      (solution_id,)
    )

    return cur.fetchone()

  @supply_cursor_if_none
  def get_fuzzy_similar_incident(
    self, violation_name: str, ruleset_name: str, incident_snip: str,
    incident_vars: dict, cur: DictCursor = None
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

    print('get_fuzzy_similar_incident')


    emb = self.emb_provider.get_embedding(incident_snip)
    emb_str = str(emb)

    incident_vars_str = json.dumps(incident_vars)

    def highest_embedding_similarity_from_all():
      cur.execute('SELECT * FROM incidents ORDER BY incident_snip_embedding <-> %s LIMIT 1;', (emb_str,))
      return dict(cur.fetchone())

    cur.execute(
      """
      SELECT v.*
      FROM violations v
      JOIN rulesets r ON v.ruleset_id = r.ruleset_id
      WHERE v.violation_name = %s
      AND r.ruleset_name = %s;
      """,
      (violation_name, ruleset_name)
    )

    violation_query = cur.fetchall()

    if len(violation_query) > 1:
      print("Ambiguous violation based on ruleset_name and violation_name")
      return highest_embedding_similarity_from_all(), 'ambiguous_violation'
    if len(violation_query) == 0:
      print(f"No violations matched: {ruleset_name=} {violation_name=}")
      return highest_embedding_similarity_from_all(), 'unseen_violation'

    violation = violation_query[0]

    cur.execute("""
      SELECT COUNT(*)
      FROM incidents
      WHERE violation_id = %s
      AND solution_id IS NOT NULL;
      """,
      (violation['violation_id'],)
    )

    number_of_slns = cur.fetchone()[0]
    if number_of_slns == 0:
      print(f"No solutions for violation: {ruleset_name=} {violation_name=}")
      return highest_embedding_similarity_from_all(), 'similarity_only'

    cur.execute("""
      SELECT *
      FROM incidents
      WHERE violation_id = %s
      AND solution_id IS NOT NULL
      AND incident_variables <@ %s
      AND incident_variables @> %s;
      """,
      (violation['violation_id'], incident_vars_str, incident_vars_str)
    )

    exact_variables_query = cur.fetchall()

    if len(exact_variables_query) == 1:
      return dict(exact_variables_query[0]), 'exact'
    elif len(exact_variables_query) == 0:
      cur.execute("""
        SELECT *
        FROM incidents
        WHERE violation_id = %s
        AND solution_id IS NOT NULL
        ORDER BY incident_snip_embedding <-> %s
        LIMIT 1;
        """,
        (violation['violation_id'], emb_str,)
      )
      return dict(cur.fetchone()), 'variables_mismatch'
    else:
      cur.execute("""
        SELECT *
        FROM incidents
        WHERE violation_id = %s
        AND solution_id IS NOT NULL
        AND incident_variables <@ %s
        AND incident_variables @> %s
        ORDER BY incident_snip_embedding <-> %s
        LIMIT 1;
        """,
        (violation['violation_id'], incident_vars_str, incident_vars_str, emb_str,)
      )
      return dict(cur.fetchone()), 'exact'


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

    number_new_incidents      = 0
    number_unsolved_incidents = 0
    number_solved_incidents   = 0

    with self.conn.cursor() as cur:
      cur.execute("DROP TABLE IF EXISTS incidents_temp;")
      cur.execute("CREATE TABLE incidents_temp (LIKE incidents INCLUDING ALL);")

      query_app = self.select_application(
        app.application_id, app.application_name, cur
      )

      if len(query_app) >= 2:
        raise Exception(f"Multiple applications found for {app}.")
      elif len(query_app) == 0 and app.application_id is not None:
        raise Exception(f"No application with application_id {app.application_id}.")
      elif len(query_app) == 0:
        application = self.insert_application(app, cur)
      else:
        application = query_app[0]

      old_commit = application['current_commit']

      report_dict = report.get_report()

      for ruleset_name, ruleset_dict in report_dict.items():
        query_ruleset = self.select_ruleset(
          ruleset_name=ruleset_name,
          # application_id=application['application_id'],
          cur=cur
        )

        if len(query_ruleset) >= 2:
          raise Exception(f"Multiple rulesets found.")
        elif len(query_ruleset) == 0:
          ruleset = self.insert_ruleset(
            ruleset_name=ruleset_name,
            # application_id=application['application_id'],
            tags=ruleset_dict.get('tags', []),
            cur=cur,
          )
        else:
          ruleset = query_ruleset[0]

        # print(f"{ruleset_name}");input()

        for violation_name, violation_dict in ruleset_dict.get('violations', {}).items():
          query_violation = self.select_violation(
            violation_name=violation_name,
            ruleset_id=ruleset['ruleset_id'],
            cur=cur
          )

          if len(query_violation) >= 2:
            raise Exception(f"Multiple rulesets found.")
          elif len(query_violation) == 0:
            violation = self.insert_violation(
              violation_name=violation_name,
              ruleset_id=ruleset['ruleset_id'],
              category=violation_dict.get('category', 'potential'),
              labels=violation_dict.get('labels', []),
              cur=cur,
            )
          else:
            violation = query_violation[0]

          # print(f"{violation_name}");input()

          for incident in violation_dict.get('incidents', []):
            # print(f"{incident['uri']=}");input()
            cur.execute(
              """INSERT INTO incidents_temp(violation_id, application_id, incident_uri, incident_snip, incident_line, incident_variables)
              VALUES (%s, %s, %s, %s, %s, %s);""",
              (
                violation['violation_id'], application['application_id'],
                incident.get('uri', ''), incident.get('codeSnip', ''),
                incident.get('lineNumber', 0),
                json.dumps(incident.get('variables', {}))
              )
            )

      # incidents_temp - incidents
      cur.execute(
        """SELECT i.incident_id AS incidents_id, it.incident_id AS incidents_temp_id, it.violation_id, it.application_id, it.incident_uri, it.incident_snip, it.incident_line, it.incident_variables
        FROM incidents_temp it
        LEFT JOIN incidents i ON it.violation_id = i.violation_id
                              AND it.application_id = i.application_id
                              AND it.incident_uri = i.incident_uri
                              AND it.incident_snip = i.incident_snip
                              AND it.incident_line = i.incident_line
                              AND it.incident_variables = i.incident_variables
        WHERE i.incident_id IS NULL;"""
      )

      new_incidents = cur.fetchall()
      number_new_incidents = len(new_incidents)

      self.conn.autocommit = False
      for ni in new_incidents:
        self.insert_incident(ni['violation_id'], ni['application_id'], ni['incident_uri'], ni['incident_snip'], ni['incident_line'], ni['incident_variables'], None, cur)
      self.conn.commit()
      cur.fetchall()
      self.conn.autocommit = True

      # incidents `intersect` incidents_temp
      cur.execute(
        """SELECT i.incident_id AS incidents_id, it.incident_id AS incidents_temp_id, i.violation_id, i.application_id, i.incident_uri, i.incident_snip, i.incident_line, i.incident_variables
        FROM incidents i
        JOIN incidents_temp it ON i.violation_id = it.violation_id
                                AND it.application_id = i.application_id
                                AND i.incident_uri = it.incident_uri
                                AND i.incident_snip = it.incident_snip
                                AND i.incident_line = it.incident_line
                                AND i.incident_variables = it.incident_variables;"""
      )

      unsolved_incidents = cur.fetchall()
      number_unsolved_incidents = len(unsolved_incidents)

      # incidents - incidents_temp
      cur.execute(
        """SELECT i.incident_id AS incidents_id, it.incident_id AS incidents_temp_id, i.violation_id, i.application_id, i.incident_uri, i.incident_snip, i.incident_line, i.incident_variables
        FROM incidents i
        LEFT JOIN incidents_temp it ON i.violation_id = it.violation_id
                                    AND it.application_id = i.application_id
                                    AND i.incident_uri = it.incident_uri
                                    AND i.incident_snip = it.incident_snip
                                    AND i.incident_line = it.incident_line
                                    AND i.incident_variables = it.incident_variables
        WHERE it.incident_id IS NULL;"""
      )

      solved_incidents = cur.fetchall()
      number_solved_incidents = len(solved_incidents)
      # print(f"# of solved inc: {len(solved_incidents)}")

      self.conn.autocommit = False
      for si in solved_incidents:
        file_path = os.path.join(repo_path, unquote(urlparse(si[4]).path).removeprefix('/tmp/source-code/'))
        big_diff = repo.git.diff(old_commit, new_commit)

        try:
          original_code = repo.git.show(f"{old_commit}:{file_path}")
        except:
          original_code = ""

        try:
          updated_code = repo.git.show(f"{new_commit}:{file_path}")
        except:
          updated_code = ""

        # file_path = pathlib.Path(os.path.join(repo_path, unquote(urlparse(si[3]).path).removeprefix('/tmp/source-code'))).as_uri()
        small_diff = repo.git.diff(old_commit, new_commit, "--", file_path)

        sln = self.insert_accepted_solution(
          app.generated_at, big_diff, small_diff, original_code, updated_code, cur
        )

        cur.execute(
          "UPDATE incidents SET solution_id = %s WHERE incident_id = %s;",
          (sln['solution_id'], si[0]))

      self.conn.commit()
      self.conn.autocommit = True

      cur.execute("DROP TABLE IF EXISTS incidents_temp;")
      application = self.update_application(application['application_id'], app, cur)

    return number_new_incidents, number_unsolved_incidents, number_solved_incidents

  # Automatic vs manual solution acceptance


  def accept_solution_from_id(self, incident_id: int, solution_id: int | None,):
    pass

  def accept_solution_from_diff():
    pass


if __name__ == '__main__':

  psqlis = PSQLIncidentStore(
    config_filepath='database.ini',
    config_section='postgresql',
    emb_provider=EmbeddingNone()
  )

  old_cmt_commit = 'c0267672ffab448735100996f5ad8ed814c38847'
  old_cmt_time   = datetime.datetime.fromtimestamp(1708003534)
  new_cmt_commit = '25f00d88f8bceefb223390dcdd656bd5af45146e'
  new_cmt_time   = datetime.datetime.fromtimestamp(1708003640)
  cmt_uri_origin = 'https://github.com/konveyor-ecosystem/cmt.git'
  cmt_uri_local  = f'file://{BASE_PATH}/samples/sample_repos/cmt'

  old_cmt_application = Application(None, 'cmt', cmt_uri_origin, cmt_uri_local, 'main',    old_cmt_commit, old_cmt_time)
  new_cmt_application = Application(None, 'cmt', cmt_uri_origin, cmt_uri_local, 'quarkus', new_cmt_commit, new_cmt_time)

  old_cmt_report = Report(f'{BASE_PATH}/samples/analysis_reports/cmt/initial/output.yaml')
  new_cmt_report = Report(f'{BASE_PATH}/samples/analysis_reports/cmt/solved/output.yaml')

  psqlis.insert_and_update_from_report(old_cmt_application, old_cmt_report)
  input("INSPECT!!")
  psqlis.insert_and_update_from_report(new_cmt_application, new_cmt_report)

  # for ruleset_name, ruleset_dict in report.get_report().items():
  #   print(f"report_dict mapping: {type(ruleset_name)} -> {type(ruleset_dict)}")

  #   for violation_name, violation_dict in ruleset_dict['violations'].items():
  #     print(f"{violation_name=} {violation_dict.keys()}")
  #   print()

  # embedding_playground(psqlis.conn, psqlis.emb_provider)

