import requests
import os
import random
from configparser import ConfigParser
from enum import Enum
from abc import ABC, abstractmethod

import psycopg2
from psycopg2.extensions import connection

import tiktoken

from InstructorEmbedding import INSTRUCTOR
import numpy
import torch


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
  def get_embedding(self,inp: str) -> list | None:
    pass

  @abstractmethod
  def get_max_tokens(self) -> int:
    pass

  @abstractmethod
  def get_dimension(self) -> int:
    pass


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


# TODO: Potentially create a Redis version of the incident store as well?
class PSQLIncidentStore:
  def __init__(
    self, *, config_filepath: str=None, config_section: str=None, 
    config: dict=None, emb_provider: EmbeddingProvider=None,
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
        raise Exception(f"Section {config_section} not found in file {config_section}.")
      
      for p in parser.items(config_section):
        config[p[0]] = p[1]


    # Embedding provider
    if emb_provider is None:
      raise Exception("emb_provider must not be None")
    
    self.emb_provider = emb_provider

    
    try:
      with psycopg2.connect(**config) as conn:
        print('Connected to the PostgreSQL server.')
        self.conn: connection = conn
        self.conn.autocommit = True

      with self.conn.cursor() as cur:
        # TODO: Figure out portable way to install the pgvector extension.
        # Containerize? "CREATE EXTENSION IF NOT EXISTS vector;" Only works as
        # superuser

        cur.execute("""
          CREATE TABLE IF NOT EXISTS solved_incidents (
            incident_id SERIAL PRIMARY KEY,
            app_name       TEXT NOT NULL,
            ruleset_name   TEXT NOT NULL,
            violation_name TEXT NOT NULL,
            incident_uri   TEXT NOT NULL,
            incident_snip  TEXT NOT NULL, 
            incident_diff  TEXT NOT NULL
          );
        """)

        # TODO: Put the embedding name in the table name?
        # - https://www.psycopg.org/docs/sql.html
        cur.execute(f"""
          CREATE TABLE IF NOT EXISTS embeddings (
            embedding_id SERIAL PRIMARY KEY,
            incident_id  INT,
            embedding    vector(%s),
            FOREIGN KEY (incident_id)
              REFERENCES solved_incidents(incident_id)
          );
        """, (self.emb_provider.get_dimension(),))

        # TODO: Flesh this out
        cur.execute("""
          CREATE TABLE IF NOT EXISTS pending_solutions (
            id SERIAL PRIMARY KEY,
            placeholder TEXT
          );
        """)
    except (psycopg2.DatabaseError, Exception) as error:
      print(error)

  
  # TODO: Batch requests as a performance optimization
  def insert_solved_incident(self, *, 
    app_name: str, ruleset_name: str, violation_name: str, incident_uri: str,
    incident_snip: str, incident_diff: str
  ) -> int | None:
    with self.conn.cursor() as cur:
      cur.execute("""
        INSERT INTO solved_incidents VALUES (%s, %s, %s, %s, %s, %s) 
        RETURNING incident_id;
      """, (app_name, ruleset_name, violation_name, incident_uri, incident_snip, incident_diff))

      rows = cur.fetchone()
      if not rows:
        return None

      incident_id = rows[0]

      # TODO: Proper rollback here and after insert if failure
      # DELETE FROM solved_incidents WHERE incident_id = "incident_id";
      embedding = self.emb_provider.get_embedding(incident_snip)
      if not embedding:
        return None
      
      cur.execute("""
        INSERT INTO embeddings VALUES (%s, %s) RETURNING embedding_id;
      """, (incident_id, str(embedding)))

      return incident_id


if __name__ == '__main__':
  psqlis = PSQLIncidentStore(
    config_filepath='database.ini', 
    config_section='postgresql',
    emb_provider=EmbeddingInstructor()
  )

  embedding_playground(psqlis.conn, psqlis.emb_provider)

