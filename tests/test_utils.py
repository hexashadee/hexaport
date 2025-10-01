# tests/test_utils.py

import unittest
from scanner.utils import parse_targets, parse_ports


class TestUtils(unittest.TestCase):

    def test_single_ip(self):
        result = parse_targets("192.168.1.1")
        self.assertEqual(result, ["192.168.1.1"])

    def test_cidr(self):
        result = parse_targets("192.168.1.0/30")
        expected = ["192.168.1.1", "192.168.1.2"]
        self.assertEqual(result, expected)

    def test_ip_range(self):
        result = parse_targets("192.168.1.10-192.168.1.12")
        expected = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
        self.assertEqual(result, expected)

    def test_short_range(self):
        result = parse_targets("192.168.1.10-12")
        expected = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
        self.assertEqual(result, expected)

    def test_parse_ports_single(self):
        result = parse_ports("80,443")
        self.assertEqual(result, [80, 443])

    def test_parse_ports_range(self):
        result = parse_ports("20-22")
        self.assertEqual(result, [20, 21, 22])

    def test_parse_ports_mixed(self):
        result = parse_ports("20-22,80,443")
        self.assertEqual(result, [20, 21, 22, 80, 443])

    def test_parse_ports_invalid(self):
        result = parse_ports("1,70000,abc,22")
        self.assertIn(1, result)
        self.assertIn(22, result)
        self.assertNotIn(70000, result)
        self.assertTrue(all(isinstance(p, int) for p in result))

    def test_invalid_ip_raises(self):
        with self.assertRaises(ValueError):
            parse_targets("999.999.999.999")

    def test_invalid_cidr_raises(self):
        with self.assertRaises(ValueError):
            parse_targets("192.168.1.0/33")


if __name__ == "__main__":
    unittest.main()
