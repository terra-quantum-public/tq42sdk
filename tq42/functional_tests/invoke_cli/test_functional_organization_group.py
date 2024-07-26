import unittest

from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliOrganizationGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def test_org_list(self):
        result = self.runner.invoke(self.cli_entry, ["org", "list"])
        assert result.exit_code == 0
        assert result.output is not None

    def test_org_set(self):
        result = self.runner.invoke(self.cli_entry, ["org", "set", self.org])
        assert result.exit_code == 0
        assert result.output is not None
