import os
import json
import subprocess
from enum import Enum
from dataclasses import dataclass

import openai
from tree_sitter import Language, Tree, Node
from monitors4codegen.multilspy import LanguageServer
from monitors4codegen.multilspy.multilspy_types import Location

class Diff:
  """
  The raw change
  """
  file: str
  raw_diff: str

@dataclass
class Change:
  """
  It's like a PR
  """
  diff: Diff
  description: str
  changes_leading_up_to_this_change: "TemporalContext"


@dataclass
class TemporalContext:
  previous_changes: list[Change]


@dataclass
class SpatialContext:
  file_before_change: str


@dataclass
class CausalContext:
  cause: str
  description: str


@dataclass
class Seed:
  """
  A seed is a location that the codeplan algorithm needs to look at, with the
  context it needs. The context is specifically for the LLM so it can do the
  smart thing
  """
  location: Location

  temporal: TemporalContext
  spatial:  SpatialContext
  causal:   CausalContext


@dataclass
class CodePlanContext:
  language_server: LanguageServer
  repository: str
  tree_sitter_language: Language

  gumtree_path: str
  tree_sitter_parser_path: str


class Classification:
  reason: str


def gumtree_diff(context: CodePlanContext, old_file: str, new_file: str):
  env = os.environ.copy()
  env['PATH'] = context.tree_sitter_parser_path + ':' + os.environ.get('PATH')
  result = subprocess.run(
    [context.gumtree_path, 'textdiff', old_file, new_file, '-g', 'java-treesitter', '-f', 'JSON'],
    stdout=subprocess.PIPE,
    env=env
  )

  actions = json.loads(result.stdout)['actions']

  # update-node


def run_codeplan(context: CodePlanContext, initial_change: Change) -> list[Diff]:
  # context = CodePlanContext(
    # language_server=,
    # repository=,
    # tree_sitter_language=,
  # )

  seeds = seeds_from_change(context, initial_change, TemporalContext())
  diffs: list[Diff] = []
  while len(seeds) > 0:
    new_seeds, diff = codeplan(context, seeds.pop(0))
    seeds.extend(new_seeds)
    diffs.append(diff)

  # Reverse the changes to the filesystem


def seeds_from_change(context: CodePlanContext, change: Change, temporal_context: TemporalContext) -> list[Seed]:
  classification = classify_change(context, change.diff)
  affected_blocks = get_affected_blocks(context, change, classification)

  temporal_context.previous_changes.append(change)
  for block in affected_blocks:
    block.temporal = temporal_context

  success = merge(context, change.diff)
  if not success:
    raise Exception(":( [get_initial_seeds: Couldn't merge change]")

  return affected_blocks + oracle(context)


def codeplan(context: CodePlanContext, seed: Seed) -> tuple[list[Seed], Change]:
  """
  Returns the list of unprocessed "next changes to make" and the change that it
  did make.
  """
  change = get_result_from_llm(seed)
  return seeds_from_change(context, change, seed.temporal), change


def classify_change(context: CodePlanContext, diff: Diff) -> Classification:
  """
  Takes ???? as input

  Process is that we take the tree before the change and the tree after the
  change, use Gumtree to find the differences (additions, modifications,
  deletions, and movings), and classify based on that.
  """

  # Apply the diff to a temp file?

  return Classification('Because I said so')


def get_affected_blocks(context: CodePlanContext, change: Change, classification: Classification) -> list[Seed]:
  pass


def merge(context: CodePlanContext, diff: Diff) -> bool:
  # TODO: Use git somehow
  pass


def oracle(context: Change) -> list[Seed]:
  return []  # TODO


def get_result_from_llm(context: CodePlanContext, seed: Seed) -> Change:
  # make prompt
  # send prompt
  # process response into structured data
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "blah blah you're a code migrator or whatever gets a good result. Also separate the diff from a description of it with `=====`"
        },
        {
            "role": "user",
            "content": seed  # TODO a representation of it
        }
    ]
  )
  content = response['choices'][0]['message']['content']
  diff, description = content.split("=====")
  return Change(diff=diff, description=description)
