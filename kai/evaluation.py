import argparse
import os
import shutil
from dataclasses import asdict, dataclass
from typing import Any

import git
import yaml

from kai.constants import PATH_BENCHMARKS
from kai.llm_io_handler import get_prompt
from kai.models.file_solution import guess_language, parse_file_solution_content
from kai.models.kai_config import KaiConfig, KaiConfigIncidentStoreSQLiteArgs
from kai.models.report_types import ExtendedIncident
from kai.report import Report
from kai.service.incident_store.incident_store import Application
from kai.service.incident_store.sqlite import SQLiteIncidentStore
from kai.service.llm_interfacing.model_provider import ModelProvider

"""
The point of this file is to automatically see if certain prompts make the
output better or worse


|      .      | Config A | Config B | ... |
|-------------|----------|----------|-----|
| Benchmark 1 | (result) | (result) |     |
| Benchmark 2 | (result) | (result) |     |
| ...         |          |          |     |
"""


@dataclass
class BenchmarkExample:
    name: str
    original_file: str
    expected_file: str
    incidents: list[ExtendedIncident]
    report: Report
    application: Application


@dataclass
class BenchmarkResult:
    prompt: str
    llm_result: str
    similarity: Any


def load_single_benchmark_example(full_example_path: str) -> BenchmarkExample:
    """
    Loads a single benchmark example from a specific directory. Contrast this
    with `load_benchmark_examples`, which loads all examples in a directory.
    """
    if not os.path.isdir(full_example_path):
        raise ValueError(f"Expected directory, got {full_example_path}")

    example_name = os.path.basename(full_example_path)
    original_file: str = None
    expected_file: str = None
    incidents: list[ExtendedIncident] = None
    report: Report = None
    application: Application = None

    for file_path in os.listdir(full_example_path):
        full_file_path = os.path.join(full_example_path, file_path)

        file_name, _ = os.path.splitext(file_path)

        if file_name == ".git":
            continue

        elif file_name == "original":
            with open(full_file_path, "r") as f:
                original_file = f.read()

        elif file_name == "expected":
            with open(full_file_path, "r") as f:
                expected_file = f.read()

        elif file_name == "incidents":
            incidents: list[ExtendedIncident] = []

            with open(full_file_path, "r") as f:
                yaml_incidents = yaml.safe_load(f)

            for yaml_incident in yaml_incidents:
                incidents.append(ExtendedIncident.model_validate(yaml_incident))

        elif file_name == "report":
            report = Report.load_report_from_file(full_file_path)

        elif file_name == "application":
            with open(full_file_path, "r") as f:
                application_file = f.read()

            application_dict = yaml.safe_load(application_file)
            application = Application(**application_dict)

    if original_file is None or expected_file is None:
        print(f"Missing original or expected file in {full_example_path}")
    if report is None:
        print(f"Missing report file in {full_example_path}")
    if application is None:
        print(f"Missing application file in {full_example_path}")

    return BenchmarkExample(
        name=example_name,
        original_file=original_file,
        expected_file=expected_file,
        report=report,
        application=application,
        incidents=incidents,
    )


DEFAULT_EXAMPLES_PATH = os.path.join(PATH_BENCHMARKS, "examples")


def load_benchmark_examples(
    examples_path=DEFAULT_EXAMPLES_PATH,
) -> dict[str, BenchmarkExample]:
    """
    Return a dict of benchmark examples, where the key is the example name. The
    benchmarks are loaded from `kai/data/benchmarks/examples` by default.

    The structure of the benchmarks directory is as follows:

    ```
    examples/
        example1/
            .git/
            original.whatever
            expected.whatever
            incidents.yaml
            application.yaml
            report.yaml
        example2/
            ...
    ```
    """

    examples: dict[str, BenchmarkExample] = {}

    for example_path in os.listdir(examples_path):
        example = load_single_benchmark_example(
            os.path.join(examples_path, example_path)
        )

        examples[example.name] = example

    return examples


def evaluate(
    configs: dict[str, KaiConfig], examples: dict[str, BenchmarkExample]
) -> dict[tuple[str, str], BenchmarkResult]:
    overall_results: dict[tuple[str, str], BenchmarkResult] = {}

    for config_path, config in configs.items():
        model_provider = ModelProvider(config.models)

        for example_path, example in examples.items():
            full_example_path = os.path.join(PATH_BENCHMARKS, "examples", example_path)
            created_git_repo = False

            try:
                if not os.path.exists(os.path.join(full_example_path, ".git")):
                    repo = git.Repo.init(full_example_path)
                    repo.index.add(".")
                    repo.index.commit("Initial commit")

                    created_git_repo = True

                incident_store = SQLiteIncidentStore(
                    KaiConfigIncidentStoreSQLiteArgs(
                        connection_string="sqlite:///:memory:"
                    ),
                    None,
                )
                incident_store.load_report(example.application, example.report)

                pb_incidents = []
                for i, incident in enumerate(example.incidents, 1):
                    pb_incident = {
                        "issue_number": i,
                        "uri": incident.uri,
                        "analysis_message": incident.analysis_message,
                        "code_snip": incident.incident_snip,
                        "analysis_line_number": incident.line_number,
                        "variables": incident.incident_variables,
                    }

                    solutions = incident_store.find_solutions(
                        incident.ruleset_name,
                        incident.violation_name,
                        incident.incident_variables,
                        incident.incident_snip,
                    )

                    if len(solutions) != 0:
                        pb_incident["solved_example_diff"] = solutions[0].file_diff
                        pb_incident["solved_example_file_name"] = solutions[0].uri

                    pb_incidents.append(pb_incident)

                src_file_language = guess_language(example.original_file)

                pb_vars = {
                    "src_file_name": example.incidents[0].uri,
                    "src_file_language": src_file_language,
                    "src_file_contents": example.original_file,
                    "incidents": pb_incidents,
                    "model_provider": model_provider,
                }

                prompt = get_prompt(
                    model_provider.template,
                    pb_vars,
                    os.path.join(PATH_BENCHMARKS, "templates"),
                )

                print(f"{example_path} - {config_path}\n{prompt[:15]}...\n")

                llm_result = model_provider.llm.invoke(prompt)
                content = parse_file_solution_content(
                    src_file_language, llm_result.content
                )

                similarity = judge_result(
                    example.expected_file,
                    content.updated_file,
                )

                overall_results[(example_path, config_path)] = BenchmarkResult(
                    similarity=similarity,
                    prompt=prompt,
                    llm_result=llm_result.content,
                )
            finally:
                if created_git_repo:
                    shutil.rmtree(os.path.join(full_example_path, ".git"))

    return overall_results


def print_nicely_formatted_comparison(results: dict[tuple[str, str], BenchmarkExample]):
    print(f'{"Example Name"}\t{"Config Name"}\t{"Benchmark Result"}')

    for (example_name, config_name), benchmark_result in results.items():
        print(f"{example_name}\t{config_name}\t{benchmark_result.similarity}")


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
    parser = argparse.ArgumentParser(description="Compare different Kai configs")

    parser.add_argument("--configs", nargs="*", help="List of configs to process")

    parser.add_argument(
        "--config_directories",
        nargs="*",
        help="List of directories, which contain multiple kai configs, to process",
    )

    parser.add_argument(
        "--output", help="Output directory for results", default="results/"
    )

    args = parser.parse_args()

    configs: dict[str, KaiConfig] = {}

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    elif os.listdir(args.output):
        raise ValueError("Output directory is not empty.")

    if args.configs is None and args.config_directories is None:
        raise ValueError("Must provide at least one config or config directory")

    if args.configs is not None:
        for full_config_filepath in args.configs:
            configs[full_config_filepath] = KaiConfig.model_validate_filepath(
                full_config_filepath
            )

    if args.config_directories is not None:
        for config_directory in args.config_directories:
            for full_config_filepath in os.listdir(config_directory):
                full_config_filepath = os.path.join(
                    config_directory, full_config_filepath
                )
                configs[full_config_filepath] = KaiConfig.model_validate_filepath(
                    full_config_filepath
                )

    examples = load_benchmark_examples()
    results = evaluate(configs, examples)

    print_nicely_formatted_comparison(results)

    for (example_name, config_name), benchmark_result in results.items():
        example_name = example_name.replace("/", "_")
        config_name = config_name.replace("/", "_")

        file_path = os.path.join(args.output, f"{config_name}.yaml")
        with open(file_path, "a") as f:
            r = asdict(benchmark_result)
            r["example_name"] = example_name
            s = yaml.safe_dump([r])
            f.write(s + "\n")


if __name__ == "__main__":
    # example: python evaluation.py --config_directories /full/path/to/kai/data/benchmarks/configs
    compare_from_cli()
