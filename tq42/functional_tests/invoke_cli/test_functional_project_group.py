import unittest

from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliProjectGroup(unittest.TestCase, FunctionalCLITestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_proj_show(self):
        args = parse_args(["proj", "show"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_proj_list(self):
        args = parse_args(["proj", "list"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

        args = parse_args(["proj", "list", "--org=" + self.org])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_proj_set(self):
        args = parse_args(["proj", "set", self.proj])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_proj_set_friendly_name(self):
        args = parse_args(
            ["proj", "set-friendly-name", "FRIENDLY_NAME", "--proj=" + self.proj]
        )
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
