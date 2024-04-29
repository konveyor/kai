# Make our own test data

# provide full kai config (params, templates, which model i'm using, etc...)

# provider = "IBMGranite"
# args = { model_id = "ibm/granite-13b-chat-v2" }

# Prompt builder stuff inside examples/prompt_engineering.ipynb

# provide multiple sets
# run it through the suite and say "hey yo this is worse or better"

import argparse
import os
import pprint
import tomllib
from dataclasses import dataclass
from typing import Callable

from kai_logging import KAI_LOG

from kai.model_provider import ModelProvider

DEFAULT_CONFIGURATION = {
    "models": {
        "provider": "IBMOpenSource",
        "args": {"model_id": "ibm-mistralai/mixtral-8x7b-instruct-v01-q"},
    }
}


@dataclass
class BenchmarkExample:
    excepted: str
    # inputs:


BENCHMARK_EXAMPLES: list[BenchmarkExample] = []


def evaluate(configs: dict[str, dict]):
    configs["default"] = DEFAULT_CONFIGURATION

    overall_results: dict[str, list] = {}

    for name, config in configs.items():
        overall_results[name] = []

        ModelProviderClass = ModelProvider.model_from_string(
            config["models"]["provider"]
        )
        model_provider = ModelProviderClass(**config["models"]["args"])

        # TODO: Make this use directories as opposed to constant
        for example in BENCHMARK_EXAMPLES:
            result = judge_result(
                example.expected,
                incident_solutions_for_file(config, example.inputs)["file"],
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

    configs = {}
    for filepath in args.filepaths:
        try:
            with open(filepath, "r") as file:
                configs[filepath] = tomllib.load(file)
        except Exception as e:
            print(f"Failed to load {filepath}: {e}")
    print_nicely_formatted_comparison(evaluate(configs))


if __name__ == "__main__":
    compare_from_cli()
