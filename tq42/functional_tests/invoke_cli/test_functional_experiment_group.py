import unittest

from tq42.project import Project
from tq42.utils.cache import clear_cache
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliExperimentGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def test_exp_list(self):
        result = self.runner.invoke(
            self.cli_entry, ["exp", "list", "--proj", self.proj]
        )

        assert result.exit_code == 0
        assert result.output is not None

        # need a default set for just running exp list
        Project(client=self.get_client(), id=self.proj).set()
        result = self.runner.invoke(self.cli_entry, ["exp", "list"])
        assert result.exit_code == 0
        assert result.output is not None
        # clear the defaults to have each test being individual
        clear_cache()

    def test_exp_set_friendly_name(self):
        result = self.runner.invoke(
            self.cli_entry,
            ["exp", "set-friendly-name", "FRIENDLY_NAME", "--exp=" + self.exp],
        )
        assert result.exit_code == 0
        assert result.output is not None
