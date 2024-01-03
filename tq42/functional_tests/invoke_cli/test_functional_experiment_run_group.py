import time
import unittest

from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.experiment_run import ExperimentRun
from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig

from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto

from tq42.exceptions import ExperimentRunCancelError


class TestFunctionalInvokeCliExperimentRunGroup(
    unittest.TestCase, FunctionalCLITestConfig
):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exp_run_list_error(self):
        args = parse_args(["exp", "run", "list"])
        self.assertRaises(SystemExit, tq42_all, self.client, args)

    def test_exp_run_list(self):
        args = parse_args(["exp", "run", "list", "--exp=" + self.exp])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_exp_run_create(self):
        parameters = '{"parameters": {"n": 2, "r": 1, "msg": "correct"}, "inputs": {}}'
        args = parse_args(
            [
                "exp",
                "run",
                "create",
                "--exp=" + self.exp,
                "--compute=SMALL",
                "--algorithm=TOY",
                "--parameters=" + parameters,
            ]
        )
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_exp_run_cancel_too_late(self):
        args = parse_args(["exp", "run", "cancel", self.exp_run])
        self.assertRaises(ExperimentRunCancelError, tq42_all, self.client, args)

    def test_exp_run_cancel(self):
        parameters = {"parameters": {"n": 2, "r": 1, "msg": "correct"}, "inputs": {}}
        exp_run = ExperimentRun.create(
            client=self.client,
            algorithm=AlgorithmProto.TOY,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )

        # we need to wait for a small bit to make sure the experiment run can be retrieved from the system
        time.sleep(5)

        args = parse_args(["exp", "run", "cancel", exp_run.id])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)

    def test_exp_run_check(self):
        args = parse_args(["exp", "run", "check", self.exp_run])
        result = tq42_all(self.client, args)
        self.assertIsNotNone(result)
