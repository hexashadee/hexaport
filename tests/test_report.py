# tests/test_report.py

import unittest
import os
import glob
from scanner.report import save_report

# Minimal scan results to test reporting
sample_results = [
    {"host": "192.168.1.1", "open_ports": [22, 80]},
    {"host": "192.168.1.2", "open_ports": []}
]


class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        os.makedirs("scan_reports", exist_ok=True)

    def tearDown(self):
        # Cleanup generated files after each test
        for file in glob.glob("scan_reports/scan_report_*"):
            os.remove(file)

    def test_save_txt_report(self):
        save_report(sample_results, format="txt")
        files = glob.glob("scan_reports/scan_report_*.txt")
        self.assertTrue(len(files) > 0)

    def test_save_csv_report(self):
        save_report(sample_results, format="csv")
        files = glob.glob("scan_reports/scan_report_*.csv")
        self.assertTrue(len(files) > 0)

    def test_save_json_report(self):
        save_report(sample_results, format="json")
        files = glob.glob("scan_reports/scan_report_*.json")
        self.assertTrue(len(files) > 0)

    def test_unsupported_format_raises(self):
        with self.assertRaises(ValueError):
            save_report(sample_results, format="xml")


if __name__ == "__main__":
    unittest.main()
