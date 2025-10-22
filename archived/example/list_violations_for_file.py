#!/usr/bin/env python

import sys

# Ensure that we have 'kai' in our import path
sys.path.append("../../kai")
from kai import Report
from kai.logging.logging import KAI_LOG

APP_NAME = "coolstore"
SAMPLE_APP_DIR = "./coolstore"

### Example to run:
# ./list_violations_for_file.py "src/main/java/com/redhat/coolstore/service/ShippingService.java"
if __name__ == "__main__":
    KAI_LOG.setLevel("info".upper())

    if len(sys.argv) < 2:
        print("Please provide a file path to list the known violations.")
        sys.exit(1)
    target_file = sys.argv[1]

    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report.load_report_from_file(coolstore_analysis_dir)
    impacted_files = r.get_impacted_files()
    violations = impacted_files.get(target_file, None)
    if not violations:
        print(f"File '{target_file}' does not have any violations")
        sys.exit(0)
    print(f"File '{target_file}' has the following violations:")
    for v in violations:
        print(f"\t{v['ruleset_name']} {v['violation_name']} at line {v['lineNumber']}")
