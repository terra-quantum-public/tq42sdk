import argparse
import unittest

import tq42.cli.cli_functions as cli
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalCli(unittest.TestCase, FunctionalCLITestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_proj_set(self):
        result = cli.set_project(self.client, self.proj)
        self.assertIsNotNone(result)

    def test_proj_show(self):
        result = cli.proj_show(self.client)
        success = "org=" in str(result)
        self.assertEqual(True, success)

    def test_list_orgs(self):
        result = cli.list_orgs(self.client)
        success = "org=" in str(result)
        self.assertEqual(True, success)

    def test_list_proj_by_org(self):
        result = cli.list_proj_by_org(self.client, self.org)
        success = "proj=" in str(result)
        self.assertEqual(True, success)

    def test_list_projects(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--org", type=str, help="Ex: 1df1f520-1834-4d3e-ac1d-65b440fd8f3c"
        )
        args = parser.parse_args(["--org", self.org])
        result = cli.list_proj_by_org(self.client, args.org)
        success = "proj=" in str(result)
        self.assertEqual(True, success)

    def test_get_exprun(self):
        result = cli.get_exprun(self.client, self.exp_run)
        success = "status" in str(result)
        self.assertEqual(True, success)
