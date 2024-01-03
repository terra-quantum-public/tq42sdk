import unittest

from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliComputeGroup(unittest.TestCase, FunctionalCLITestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_list(self):
        args = parse_args(["compute", "list"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_compute_show_details(self):
        args = parse_args(["compute", "show-details"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_compute_show_details_small(self):
        args = parse_args(["compute", "show-details", "--compute=SMALL"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_compute_show_details_small_gpu(self):
        args = parse_args(["compute", "show-details", "--compute=SMALL_GPU"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_compute_show_details_large(self):
        args = parse_args(["compute", "show-details", "--compute=LARGE"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_compute_show_details_large_gpu(self):
        args = parse_args(["compute", "show-details", "--compute=LARGE_GPU"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
