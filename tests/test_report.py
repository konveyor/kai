import os
import pprint
import unittest
from pathlib import Path

from kai.models.report import Report
from kai.models.report_types import ExtendedIncident


class TestReports(unittest.TestCase):

    def get_coolstuff_yaml(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "test_data/coolstuff.yaml")

    def test_create_with_bad_path(self):
        with self.assertRaises(FileNotFoundError):
            Report.load_report_from_file("bad_path")

    def test_parse(self):
        report = dict(Report.load_report_from_file(self.get_coolstuff_yaml()))
        self.assertTrue(report is not None)

    def test_impacted_files(self):
        pprint.PrettyPrinter(indent=2)
        rObj = Report.load_report_from_file(self.get_coolstuff_yaml())
        self.assertTrue(rObj is not None)
        impacted_files = rObj.get_impacted_files()
        for f in impacted_files.keys():
            print(f"File: `{f}` has {len(impacted_files[f])} violations")
        # pp.pprint(impacted_files)
        # print(f"Found {len(impacted_files)} impacted files")
        # print(f"Found {impacted_files.keys()}")
        self.assertTrue(len(impacted_files) == 25)
        test_file_entry = Path(
            "src/main/java/com/redhat/coolstore/model/InventoryEntity.java"
        )
        self.assertTrue(test_file_entry in impacted_files)
        test_entry = impacted_files[test_file_entry]
        self.assertTrue(len(test_entry) == 6)
        self.assertTrue(isinstance(test_entry[0], ExtendedIncident))


if __name__ == "__main__":
    unittest.main()
