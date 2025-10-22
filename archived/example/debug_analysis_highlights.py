#!/usr/bin/env python

# Ensure that we have 'kai' in our import path
import sys

sys.path.append("../../kai")

from kai.analyzer_types import Report

# TODOs
# 1) Add Types via Typing
# 2) Display summary of Analysis
# 3) Display highlights of the specific Rules we are interested in


def print_impacted_files(report):
    impacted_files = report.get_impacted_files()
    # This will print out the impacted files and the violations that were found in them
    for file_path, violations in impacted_files.items():
        print(f"File: {file_path} has {len(violations)} violations.")
        # for violation in violations:
        # print(f"  Violation: {violation['violation_name']}\n")
        # print(f"  Message: {violation['message']}")
        # print(f"  Code Snippet: {violation['codeSnip']}")
        # print(f"  Line Number: {violation['lineNumber']}")
        # print("\n")


if __name__ == "__main__":
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report.load_report_from_file(coolstore_analysis_dir)
    markdown_dir = "./analysis/coolstore/markdown/"
    print(f"\n\nAnalysis summary will be written in markdown to: {markdown_dir} \n\n")
    r.write_markdown(markdown_dir)
    print_impacted_files(r)
