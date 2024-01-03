import unittest

from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliOrganizationGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_org_list(self):
        args = parse_args(["org", "list"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_org_set(self):
        args = parse_args(["org", "set", self.org])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
