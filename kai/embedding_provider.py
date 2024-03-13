import argparse
import datetime
import json
import os
import random
from abc import ABC, abstractmethod
from configparser import ConfigParser
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from inspect import signature
from urllib.parse import unquote, urlparse

import numpy
import psycopg2
import requests
import tiktoken
import torch
import yaml
from git import Repo
from InstructorEmbedding import INSTRUCTOR
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor, DictRow
from report import Report


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
        self.dimension = 1

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

    def __init__(
        self, openai_api_key: str, model: str = "text-embedding-3-small"
    ) -> None:
        self.max_tokens = 8192
        self.dimension = 1536

        self.openai_api_key = openai_api_key
        self.model = "text-embedding-3-small"

    def get_embedding(self, inp: str) -> list | None:
        enc = tiktoken.encoding_for_model(self.model)
        toks = trim_list(enc.encode(inp), self.max_tokens)
        dec = enc.decode(toks)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
        }

        data = {"input": dec, "model": "text-embedding-3-small"}

        response: requests.Response = requests.post(
            "https://api.openai.com/v1/embeddings", json=data, headers=headers
        )

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return None

        return response.json()["data"][0]["embedding"]

    def get_max_tokens(self) -> int:
        return self.max_tokens

    def get_dimension(self) -> int:
        return self.dimension


class EmbeddingInstructor(EmbeddingProvider):
    """
    - link: https://huggingface.co/hkunlp/instructor-xl
    """

    def __init__(self, model: str = "hkunlp/instructor-large") -> None:
        # It appears instructor cuts off all tokens after the 512 mark automatically

        self.max_tokens = 512  # TODO: find out
        self.dimension = 768

        self.instructor = INSTRUCTOR(model)

    def get_embedding(self, inp: str) -> list | None:
        prompt = [["Represent the source code file for semantic similarity", inp]]
        toks = self.instructor.tokenize([inp])["input_ids"].tolist()[0]

        if len(toks) > self.max_tokens:
            print(f"Length of tokens is {len(toks)}. Truncating to {self.max_tokens}.")

        result: numpy.ndarray = self.instructor.encode(prompt).tolist()[0]
        return result

    def get_dimension(self) -> int:
        return self.dimension

    def get_max_tokens(self) -> int:
        return self.max_tokens


def embedding_playground(conn: connection, embp: EmbeddingProvider) -> None:
    table_name = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(30))

    with conn.cursor() as cur:
        # I know, string interpolation in SQL. But this is a playground, not for
        # production!
        cur.execute(
            f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
      id SERIAL PRIMARY KEY,
      the_text TEXT,
      embedding vector(%s)
    )
    """,
            (embp.get_dimension(),),
        )

        while True:
            try:
                inp = input("> ")
                emb = embp.get_embedding(inp)
                cur.execute(
                    f"""
          INSERT INTO {table_name}(the_text, embedding)
          VALUES (%s, %s)
        """,
                    (
                        inp,
                        str(emb),
                    ),
                )

                cur.execute(
                    f"SELECT the_text FROM {table_name} ORDER BY embedding <=> %s LIMIT 25;",
                    (str(emb),),
                )

                for row in cur.fetchall():
                    print(row)
                print()

            except KeyboardInterrupt:
                cur.execute(f"DROP TABLE {table_name};")
                break
