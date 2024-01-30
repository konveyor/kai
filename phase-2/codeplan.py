import os
import re
import json
import shutil
import pathlib
import tempfile
import subprocess
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from urllib.parse import urlparse

import openai
from tree_sitter import Language, Tree, Node, Parser
from monitors4codegen.multilspy import LanguageServer
from monitors4codegen.multilspy.multilspy_types import Location, Range, Position

@dataclass
class Change:
  """
  It's like a PR
  """
  diff: str
  uri: str
  description: str
  temporal: "TemporalContext"


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
  A seed is a location that the CodePlan algorithm needs to look at, with the
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
  repo_path: str
  ts_language: Language
  
  gumtree_path: str
  tree_sitter_parser_path: str


class Classification:
  reason: str

def is_within_range(range: Range, pos: Position):
  if range["start"]["line"] < pos["line"] < range["end"]["line"]:
    return True
  elif pos["line"] == range["start"]["line"] and pos["line"] == range["end"]["line"]:
    return range["start"]["character"] <= pos["character"] <= range["end"]["character"]
  elif pos["line"] == range["start"]["line"]:
    return pos["character"] >= range["start"]["character"]
  elif pos["line"] == range["end"]["line"]:
    return pos["character"] <= range["end"]["character"]
  else:
    return False
  
# To diff two files:
# `git diff --no-index <file_a> <file_b>`
# To apply a patch:
# stdin > `patch -p0 -s -o -`

def run_codeplan(ctx: CodePlanContext, initial_change: Change) -> str:
  git_cmd = ['git', '--git-dir=.git-kai', '--work-tree=.']
  setup = [
    ['init'],
    ['add', '.'],
    ['commit', '-m', 'KAI commit'],
  ]
  for cmd in setup:
    subprocess.run(git_cmd + cmd, cwd=ctx.repo_path, check=True)

  seeds: list[Seed] = get_affected_blocks(initial_change)
  if not merge(change):
    raise Exception("run_codeplan: couldn't merge initial change")
  
  # with temp file

  while seeds:
    seed = seeds.pop(0)
    prompt = construct_prompt(seed)
    change = get_result_from_llm(prompt)
    blocks = get_affected_blocks(change)

    if not merge(change):
      raise Exception("run_codeplan: couldn't merge change")
    
    seeds.extend(blocks)
    
  git_diff = subprocess.run(git_cmd + ['diff'], stdout=subprocess.PIPE).stdout

  # undo changes
  teardown = [
    ['add', '.'],
    ['commit', '-m', 'KAI commit'],
    ['reset', 'HEAD~1'],
  ]
  for cmd in teardown:
    subprocess.run(git_cmd + cmd, cwd=ctx.repo_path, check=True)

  shutil.rmtree(os.path.join(ctx.repo_path, '.git-kai'))

  return git_diff


# def run_codeplan(context: CodePlanContext, initial_change: Change) -> list[Diff]:
#   seeds = seeds_from_change(context, initial_change, TemporalContext())
#   diffs: list[Diff] = []
#   while len(seeds) > 0:
#     seed = seeds.pop(0)
#     change = get_result_from_llm(seed)
#     seeds.extend(seeds_from_change(context, change, seed.temporal))
#     diffs.append(change.diff)

#   # TODO: Reverse the changes to the filesystem
    
#   return diffs
  

# def seeds_from_change(context: CodePlanContext, change: Change, temporal_context: TemporalContext) -> list[Seed]:
#   classification = classify_change(context, change.diff)
#   affected_blocks = get_affected_blocks(context, change, classification)

#   temporal_context.previous_changes.append(change)
#   for block in affected_blocks:
#     block.temporal = temporal_context
  
#   success = merge(context, change.diff)
#   if not success:
#     raise Exception(":( [get_initial_seeds: Couldn't merge change]")
  
#   return affected_blocks + oracle(context)


# def codeplan(context: CodePlanContext, seed: Seed) -> tuple[list[Seed], Change]:
#   """
#   Returns the list of unprocessed "next changes to make" and the change that it
#   did make.
#   """
#   change = get_result_from_llm(seed)
#   return seeds_from_change(context, change, seed.temporal), change


# def classify_change(context: CodePlanContext, diff: Diff) -> Classification:
#   """
#   Takes ???? as input

#   Process is that we take the tree before the change and the tree after the
#   change, use Gumtree to find the differences (additions, modifications,
#   deletions, and movings), and classify based on that.
#   """
  
#   # Apply the diff to a temp file?

#   return Classification('Because I said so')

def parse_gumtree_output(gumtree_output: str) -> list[dict]:
  output: list[dict] = []

  sections = gumtree_output.split('===\n')

  for section in filter(None, sections):
    pieces = section.split('---\n')
    if len(pieces) != 2: continue # TODO: Silently fail for now

    action, argument = pieces[0].strip(), pieces[1].strip()
    if action == 'match': continue

    arguments = argument.split('\n')

    type_tuple_pattern = r'^(.*?)\s\[(\d+),(\d+)\]$'
    at_pattern         = r'^(.*?)\s(\d+)$'
    replace_by_pattern = r'^replace\s(.*?)\sby\s(.*)$'

    m = re.search(type_tuple_pattern, arguments[0])
    if not m: continue

    node = {
      'type':       str(m.group(1)),
      'start_byte': int(m.group(2)),
      'end_byte':   int(m.group(3)),
    }

    # NOTE: gumtree returns some funky stuff in `type` with `update-node`
    if action == 'update-node':
      m = re.search(replace_by_pattern, arguments[-1])
      old, new = m.group(1), m.group(2)

      output.append({'action': action, 'old_node': node, 'old_text': old, 'new_text': new})

    elif action == 'insert-tree' or action == 'move-tree':
      m = re.search(type_tuple_pattern, arguments[-2])
      to = {
        'type':       str(m.group(1)),
        'start_byte': int(m.group(2)),
        'end_byte':   int(m.group(3)),
      }
      
      m = re.search(at_pattern, arguments[-1])
      at = int(m.group(2))

      output.append({'action': action, 'new_node': node, 'old_node': to, 'at': at})
     
    elif action == 'delete-node':
      output.append({'action': action, 'old_node': node})

    else:
      raise Exception(f"parse_gumtree_output: unhandled action `{action}`")

  return output


def get_node_with_exact_range(node: Node, start_byte: int, end_byte: int):
  if node.start_byte == start_byte and node.end_byte == end_byte:
    return node
  for child in node.children:
    if result := get_node_with_exact_range(child, start_byte, end_byte):
      return result
  return None

# def get_affected_blocks(context: CodePlanContext, change: Change, classification: Classification) -> list[Seed]:
async def get_affected_blocks(context: CodePlanContext, change: Change) -> list[Seed]:
  # TODO: Node ticketing. Split this function up? 
  output: list[Seed] = []

  parser = Parser()
  parser.set_language(context.ts_language)

  before_path: str = urlparse(change.uri).path
  after_path: str

  # print(f"{before_path=}")

  before_contents: str = pathlib.Path(before_path).read_text()
  after_contents:  str = subprocess.run(
    ['patch', '-s', '-o', '-', before_path], 
    input=change.diff.encode(), stdout=subprocess.PIPE,
  ).stdout.decode()

  before_tree = parser.parse(bytes(before_contents, 'utf-8'))
  after_tree = parser.parse(bytes(after_contents, 'utf-8'))

  print(f"{before_contents=}\n{after_contents=}")

  new_temporal_context = change.temporal
  new_temporal_context.previous_changes.append(change)

  with tempfile.NamedTemporaryFile(mode='w+t') as tmp:
    tmp.write(after_contents)
    tmp.seek(0)

    env = os.environ.copy()
    env['PATH'] = context.tree_sitter_parser_path + ':' + os.environ.get('PATH')
    raw_gumtree_output = subprocess.run(
      [context.gumtree_path, 'textdiff', before_path, tmp.name, '-g', 'java-treesitter'], 
      stdout=subprocess.PIPE, 
      env=env,
    ).stdout.decode()

    gumtree_output = parse_gumtree_output(raw_gumtree_output)

    break_types = ['field_declaration']

    for element in gumtree_output:
      old_node = get_node_with_exact_range(
        before_tree.root_node, 
        element['old_node']['start_byte'],
        element['old_node']['end_byte']
      )
      if old_node == None:
        raise Exception(f"get_affected_blocks: No node in before_tree with range [{element['old_node']['start_byte']}, {element['old_node']['end_byte']}]")

      # TODO: fix this
      kind: str
      if element['action'] == 'move-tree':
        continue
      elif element['action'] == 'update-node':
        kind = "modified"
      elif element['action'] == 'insert-tree':
        kind = "added"
      elif element['action'] == 'delete-node':
        kind = "removed"
      else:
        raise Exception(f"get_affected_blocks: unhandled gumtree action `{element['action']}`")
      
      break_node = old_node
      while break_node and (break_node.type not in break_types):
        break_node = break_node.parent

      if not break_node:
        raise Exception(f"get_affected_blocks: old_node didn't have a 'good' parent")
      
      if break_node.type == 'field_declaration':
        line, char = break_node.child_by_field_name('declarator').end_point

        refs = await (context.language_server.request_references(
          change.uri[len(f"file://{context.repo_path}"):],
          line,
          char
        ))
        
        for ref in refs:
          if is_within_range(Range(**ref['range']), Position(line=line, character=char)):
            continue

          output.append(Seed(
            location=Location(uri=ref['uri'], range=ref['range']),
            temporal=new_temporal_context,
            spatial=SpatialContext(
              file_before_change=after_contents,
            ),
            causal=CausalContext(
              cause=f"field was {kind}",
              description="",
            ),
          ))

      else:
        # TODO: remove this once we've added all the break types
        raise Exception(f"get_affected_blocks: unhandled break_node type `{break_node.type}`")

  return output



def merge(context: CodePlanContext, change: Change) -> bool:
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