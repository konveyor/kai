__version__ = "0.0.1"

from typing import Annotated, List

import typer

from kai.incident_store import IncidentStore
from kai.report import Report
from kai.result import LLMResult

# from typing_extensions import Annotated


app = typer.Typer()

# report_app = typer.Typer()
# result_app = typer.Typer()

# app.add_typer(report_app, name="report", help="Generate a markdown report from a raw analysis yaml.")
# app.add_typer(result_app, name="result", help="Generate patches for given violations and incidents from an analysis yaml")


@app.command()
def report(analysis_path: str, output_dir: str):
    """
    Generate a Markdown report of a given analysis
    YAML to be read by a human
    """
    report = Report(analysis_path)
    r = report.get_report()
    print(f"We have results from {len(r.keys())} RuleSet(s) in {analysis_path}\n")
    report.write_markdown(output_dir)


@app.command()
def generate(
    path_to_report: str,
    path_to_source: str,
    example_initial_branch: str,
    example_solved_branch: str,
    path_to_output: str,
    limit_rulesets: Annotated[List[str], typer.Option("--ruleset", "-r")] = None,
    limit_violations: Annotated[List[str], typer.Option("--violation", "-v")] = None,
    model: Annotated[str, typer.Option("--model", "-m")] = "gpt-3.5-turbo-16k",
):
    # model: Annotated[Optional[str], typer.Argument()] = "gpt-3.5-turbo-16k"):
    """
    Generate patches for given violations and incidents from an analysis yaml report

    - path_to_report: Path to the analysis yaml report

    - path_to_source: Path to the source code to be patched

    - example_initial_branch: Branch name for the initial state of the source code

    - example_solved_branch: Branch name for the solved state of the source code

    - path_to_output: Path to the output directory for the patches

    - limit_rulesets: Limit to specific rulesets (defaults to 'None', meaning to run all)

    - limit_violations: Limit to specific violations (defaults to 'None', meaning to run all)

    - model: Model name to use for generating the patches (defaults to 'gpt-3.5-turbo-16k', 'gpt-4-1106-preview' is another good option)
    """
    print(
        f"Generating patches for {path_to_report} for example app at {path_to_source}"
    )
    print(f"Initial branch: {example_initial_branch}")
    print(f"Solved branch: {example_solved_branch}")
    print(f"Output directory: {path_to_output}")
    print(f"Model: {model}")
    print(f"Limit to ruleset(s): {limit_rulesets}")
    print(f"Limit to violation(s): {limit_violations}")

    llmResult = LLMResult(path_to_source, example_initial_branch, example_solved_branch)
    llmResult.parse_report(path_to_report)
    llmResult.process(path_to_output, model, limit_rulesets, limit_violations)
    print(f"Completed processing, output written to {path_to_output}\n")


@app.command()
def load(folder_path: str):
    """
    Load the incident store with the given applications
    write the cached_violations to a file for later use
    """
    incident_store = IncidentStore()
    incident_store.load_incident_store(folder_path)


@app.command()
def patch(ruleset: str, violation: str):
    """
    Generate patches for a specific violation
    """
    print(f"Generating patches for {ruleset} - {violation}")
    incident_store = IncidentStore()
    patches = incident_store.get_solved_issue(ruleset, violation)
    if len(patches) == 0:
        print(f"No patches found for {ruleset} - {violation}")
    else:
        for patch in patches:
            print(f"Patch: {patch}")
    return patches


@app.command()
def common(ruleset: str, violation: str):
    """
    Find common violations for a specific violation
    """
    print(f"Finding common violations for {ruleset} - {violation}")
    incident_store = IncidentStore()
    violations = incident_store.find_common_violations(ruleset, violation)
    if violations is None:
        print(f"No common violations found for {ruleset} - {violation}")
    for violation in violations:
        print(f"Violation: {violation}")
    return violations
