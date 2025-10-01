# tests/test_core.py

import unittest
from scanner.core import scan_port, scan_host, run_scan


class TestCoreScanner(unittest.TestCase):

    def test_scan_known_closed_port(self):
        # High ports are often closed; change if needed
        result = scan_port("127.0.0.1", 65000)
        self.assertFalse(result)

    def test_scan_known_open_or_closed_port(self):
        # Common port — may or may not be open depending on system
        result = scan_port("127.0.0.1", 22)
        self.assertIn(result, [True, False])  # Just ensure it runs

    def test_scan_host(self):
        ports = [22, 65000]
        result = scan_host("127.0.0.1", ports)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["host"], "127.0.0.1")
        self.assertIn("open_ports", result)

    def test_run_scan(self):
        targets = ["127.0.0.1"]
        ports = [22, 65000]
        results = run_scan(targets, ports, max_threads=5)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertIn("host", results[0])
        self.assertIn("open_ports", results[0])


if __name__ == "__main__":
    unittest.main()
