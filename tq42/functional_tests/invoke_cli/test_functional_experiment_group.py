import unittest

from tq42.project import Project
from tq42.utils.utils_for_cache import clear_cache
from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliExperimentGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exp_list(self):
        args = parse_args(["exp", "list", "--proj=" + self.proj])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

        # need a default set for just running exp list
        Project(client=self.get_client(), id=self.proj).set()
        args = parse_args(["exp", "list"])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
        # clear the defaults to have each test being individual
        clear_cache()

    def test_exp_set_friendly_name(self):
        args = parse_args(
            ["exp", "set-friendly-name", "FRIENDLY_NAME", "--exp=" + self.exp]
        )
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
