import unittest

from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalCli(unittest.TestCase, FunctionalCLITestConfig):
    def test_proj_set(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "set", self.proj])
        assert result is not None

    def test_proj_show(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "show"])
        assert result.exit_code == 0
        assert "org=" in result.output

    def test_list_orgs(self):
        result = self.runner.invoke(self.cli_entry, ["org", "list"])
        assert "org=" in result.output

    def test_list_proj_by_org(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "list", "--org", self.org])
        assert "proj=" in result.output

    def test_get_exprun(self):
        result = self.runner.invoke(
            self.cli_entry, ["exp", "run", "check", self.exp_run]
        )
        assert "status" in result.output
