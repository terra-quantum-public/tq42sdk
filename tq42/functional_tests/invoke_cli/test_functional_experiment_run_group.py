import time
import unittest

from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliExperimentRunGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def test_exp_run_list_should_error_if_no_exp_run_id_is_given(self):
        result = self.runner.invoke(self.cli_entry, ["exp", "run", "list"])
        assert result.exit_code == 2

    def test_exp_run_list(self):
        result = self.runner.invoke(
            self.cli_entry, ["exp", "run", "list", "--exp=" + self.exp]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_exp_run_create(self):
        parameters = '{"parameters": {"n": 2, "r": 1, "msg": "correct"}, "inputs": {}}'
        result = self.runner.invoke(
            self.cli_entry,
            [
                "exp",
                "run",
                "create",
                "--exp=" + self.exp,
                "--compute=SMALL",
                "--algorithm=TOY",
                "--version=0.1.0",
                "--parameters=" + parameters,
            ],
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_exp_run_cancel_should_error_too_late(self):
        result = self.runner.invoke(
            self.cli_entry, ["exp", "run", "cancel", self.exp_run]
        )
        assert result.exit_code == 1

    def test_exp_run_cancel_happy_path(self):
        parameters = {"parameters": {"n": 2, "r": 1, "msg": "correct"}, "inputs": {}}
        exp_run = ExperimentRun.create(
            client=self.client,
            algorithm="TOY",
            version="0.1.0",
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )

        # we need to wait for a small bit to make sure the experiment run can be retrieved from the system
        time.sleep(5)

        result = self.runner.invoke(
            self.cli_entry, ["exp", "run", "cancel", exp_run.id]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_exp_run_check(self):
        result = self.runner.invoke(
            self.cli_entry, ["exp", "run", "check", self.exp_run]
        )
        assert result.exit_code == 0
        assert result.output is not None
