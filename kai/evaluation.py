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
from typing import Any, Optional

import yaml
from pydantic import BaseModel

from kai.model_provider import ModelProvider
from kai.models.analyzer_types import Incident
from kai.models.file_solution import guess_language, parse_file_solution_content
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


# NOTE(@JonahSussman): I so desperately want to have this inherit from
# `BaseModel`, but I can't for some reason.
@dataclass
class BenchmarkConfiguration:
    model_config: KaiConfigModels
    override_template: Optional[str]


@dataclass
class BenchmarkExample:
    original_file: str
    expected_file: str
    incidents: list[Incident]


@dataclass
class BenchmarkResult:
    prompt: str
    llm_result: str
    similarity: Any


def load_benchmarks(
    benchmarks_path=os.path.join(os.path.dirname(__file__), "data", "benchmarks")
) -> tuple[dict[str, BenchmarkConfiguration], dict[str, BenchmarkExample]]:
    examples_path = os.path.join(benchmarks_path, "examples")
    configs_path = os.path.join(benchmarks_path, "configs")

    configs: dict[str, BenchmarkConfiguration] = {}
    examples: dict[str, BenchmarkExample] = {}

    for example_path in os.listdir(examples_path):
        full_example_path = os.path.join(examples_path, example_path)

        # Directory structure is as follows:
        #
        #   example1/
        #     original.whatever
        #     expected.whatever
        #     incidents.yaml
        #   example2/
        #    ...

        if not os.path.isdir(full_example_path):
            raise ValueError(f"Expected directory, got {full_example_path}")

        original_file: str = None
        expected_file: str = None
        incidents: list[Incident] = None

        for file_path in os.listdir(full_example_path):
            full_file_path = os.path.join(full_example_path, file_path)

            file_name, _ = os.path.splitext(file_path)

            if file_name == "original":
                with open(full_file_path, "r") as f:
                    original_file = f.read()
            elif file_name == "expected":
                with open(full_file_path, "r") as f:
                    expected_file = f.read()
            elif file_name == "incidents":
                incidents: list[Incident] = []

                with open(full_file_path, "r") as f:
                    yaml_incidents = yaml.safe_load(f)

                for yaml_incident in yaml_incidents:
                    incidents.append(Incident.model_validate(yaml_incident))

            else:
                raise ValueError(
                    f"File must be either `original`, `expected`, or `incidents` in {example_path}. Got `{file_name}`."
                )

        if original_file is None or expected_file is None:
            raise ValueError(
                f"Missing original or expected file in {full_example_path}"
            )
        if incidents is None:
            raise ValueError(f"Missing incidents file in {full_example_path}")

        examples[example_path] = BenchmarkExample(
            original_file, expected_file, incidents
        )

    for config_path in os.listdir(configs_path):
        config_name, _ = os.path.splitext(config_path)
        full_config_path = os.path.join(configs_path, config_path)

        with open(full_config_path, "r") as f:
            data: dict = yaml.safe_load(f)

            if set(data.keys()) != {"model_config", "override_template"}:
                raise ValueError(
                    f"Expected keys `model_config` and `override_template` in {full_config_path}. Got {data.keys()}"
                )

            config = BenchmarkConfiguration(
                model_config=KaiConfigModels.model_validate(data["model_config"]),
                override_template=data["override_template"],
            )

            configs[config_name] = config

    return (configs, examples)


def evaluate(
    configs: dict[str, BenchmarkConfiguration], examples: dict[str, BenchmarkExample]
):
    overall_results: dict[tuple[str, str], Any] = {}

    for config_name, config in configs.items():
        overall_results[config_name] = []
        model_provider = ModelProvider(config.model_config)

        for example_name, example in examples.items():
            # TODO(@JonahSussman): Change this after the prompt builder refactor

            pb_incidents = []
            for i, incident in enumerate(example.incidents, 1):
                pb_incidents.append(
                    {
                        "issue_number": i,
                        "uri": incident.uri,
                        "analysis_message": incident.analysis_message,
                        "code_snip": incident.incident_snip,
                        "analysis_line_number": incident.line_number,
                        "variables": incident.incident_variables,
                    }
                )

            src_file_language = guess_language(example.original_file)

            pb_vars = {
                "src_file_name": example.incidents[0].uri,
                "src_file_language": src_file_language,
                "src_file_contents": example.original_file,
                "incidents": pb_incidents,
            }

            prompt = build_prompt(
                model_provider.get_prompt_builder_config("multi_file"), pb_vars
            )

            print(f"{config_name} - {example_name}\n{prompt}\n")

            llm_result = model_provider.llm.invoke(prompt)
            content = parse_file_solution_content(src_file_language, llm_result.content)

            similarity = judge_result(
                example.expected_file,
                content.updated_file,
            )

            overall_results[(example_name, config_name)] = BenchmarkResult(
                similarity=similarity,
                prompt=prompt,
                llm_result=llm_result,
            )

            # overall_results[f"{config_name}/{example_name}"] = {
            #     "similarity": similarity,
            #     "prompt": prompt,
            #     "llm_result": llm_result.content,
            #     "updated_file": content.updated_file,
            # }

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


# def compare_from_cli():
#     parser = argparse.ArgumentParser(description="Process a list of filepaths.")
#     parser.add_argument("filepaths", nargs="+", help="List of filepaths to process")

#     args = parser.parse_args()

#     configs: dict[str, BenchmarkConfiguration] = {}
#     for filepath in args.filepaths:
#         try:
#             with open(filepath, "r") as f:
#                 configs[filepath] = KaiConfigModels.model_validate(yaml.safe_load(f))

#         except Exception as e:
#             print(f"Failed to load {filepath}: {e}")

#     print_nicely_formatted_comparison(evaluate(configs))


if __name__ == "__main__":
    configs, examples = load_benchmarks()
    results = evaluate(configs, examples)

    import json

    print(json.dumps(results))
