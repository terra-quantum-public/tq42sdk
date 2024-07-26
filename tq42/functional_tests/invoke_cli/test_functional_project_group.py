import unittest

from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliProjectGroup(unittest.TestCase, FunctionalCLITestConfig):
    def test_proj_show(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "show"])
        assert result.exit_code == 0
        assert result.output is not None

    def test_proj_list(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "list"])
        assert result.exit_code == 0
        assert result.output is not None

    def test_proj_list_with_org_parameter(self):
        result = self.runner.invoke(
            self.cli_entry, ["proj", "list", "--org=" + self.org]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_proj_set(self):
        result = self.runner.invoke(self.cli_entry, ["proj", "set", self.proj])
        assert result.exit_code == 0
        assert result.output is not None

    def test_proj_set_friendly_name(self):
        result = self.runner.invoke(
            self.cli_entry,
            ["proj", "set-friendly-name", "FRIENDLY_NAME", "--proj=" + self.proj],
        )
        assert result.exit_code == 0
        assert result.output is not None
