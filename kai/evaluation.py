# Make our own test data

# provide full kai config (params, templates, which model i'm using, etc...)

# provider = "IBMGranite"
# args = { model_id = "ibm/granite-13b-chat-v2" }

# Prompt builder stuff inside examples/prompt_engineering.ipynb

# provide multiple sets
# run it through the suite and say "hey yo this is worse or better"

import argparse
import os
import tomllib
from dataclasses import dataclass
from typing import Optional

import yaml
from pydantic import BaseModel

from kai import prompt_builder
from kai.model_provider import ModelProvider
from kai.models.kai_config import KaiConfigModels
from kai.prompt_builder import build_prompt

"""
The point of this file is to automatically see if certain prompts make the
output better or worse


|      .      | Config A | Config B | ... |
|-------------|----------|----------|-----|
| Benchmark 1 | (result) | (result) |     |
| Benchmark 2 | (result) | (result) |     |
| ...         |          |          |     |
"""


class BenchmarkConfiguration(BaseModel):
    model_config: KaiConfigModels
    override_template: Optional[str]


DEFAULT_CONFIGURATION = BenchmarkConfiguration(
    model_config=KaiConfigModels.model_validate(
        {
            "models": {
                "provider": "ChatIBMGenAI",
                "args": {"model_id": "ibm-mistralai/mixtral-8x7b-instruct-v01-q"},
            }
        }
    ),
    override_template=None,
)


@dataclass
class BenchmarkExample:
    original_file: str
    expected_file: str


def load_benchmarks(
    benchmarks_path=os.path.join(os.path.dirname(__file__), "data", "benchmarks")
) -> tuple[list[BenchmarkConfiguration], list[BenchmarkExample]]:

    examples_path = os.path.join(benchmarks_path, "examples")
    configs_path = os.path.join(benchmarks_path, "configs")

    configs = []
    examples = []

    for example_path in os.listdir(examples_path):
        full_example_path = os.path.join(examples_path, examples_path)

    for config_path in os.listdir(configs_path):
        full_config_path = os.path.join(configs_path, config_path)

        with open(full_config_path, "r") as f:
            data = yaml.safe_load(f)
            config = BenchmarkConfiguration.model_validate(data)
            configs.append(config)

    return (configs, examples)


def evaluate(configs: dict[str, BenchmarkConfiguration]):
    configs["default"] = DEFAULT_CONFIGURATION

    overall_results: dict[str, list] = {}

    for name, config in configs.items():
        overall_results[name] = []

        model_provider = ModelProvider(config)

        # TODO: Make this use directories as opposed to constant
        for example in load_benchmarks():
            pb_vars = {
                "src_file_name": file_name,
                "src_file_language": src_file_language,
                "src_file_contents": updated_file,
                "incidents": incidents,
            }

            prompt = build_prompt(
                model_provider.get_prompt_builder_config("multi_file")
            )
            model_provider.llm.invoke()

            result = judge_result(
                example.expected,
                # incident_solutions_for_file(config, example.inputs)["file"],
            )
            overall_results[name].append(result)

    return overall_results


def print_nicely_formatted_comparison(results: dict[str, list]):
    for name, result_list in results:
        print(name)
        print("---")

        for i, result in enumerate(result_list):
            print(f"{i:03d}: {result}")


def judge_result(expected_file: str, actual_file: str) -> float:
    return levenshtein_distance(expected_file, actual_file)


def levenshtein_distance(s1, s2) -> float:
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                )
        distances = distances_

    return float(distances[-1])


def compare_from_cli():
    parser = argparse.ArgumentParser(description="Process a list of filepaths.")
    parser.add_argument("filepaths", nargs="+", help="List of filepaths to process")

    args = parser.parse_args()

    configs: dict[str, BenchmarkConfiguration] = {}
    for filepath in args.filepaths:
        try:
            with open(filepath, "r") as f:
                configs[filepath] = KaiConfigModels.model_validate(yaml.safe_load(f))

        except Exception as e:
            print(f"Failed to load {filepath}: {e}")

    print_nicely_formatted_comparison(evaluate(configs))


if __name__ == "__main__":
    compare_from_cli()
