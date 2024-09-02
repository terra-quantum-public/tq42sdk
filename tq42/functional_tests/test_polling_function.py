import unittest
from pytest import mark

from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)


@mark.poll
class TestFunctionalPollingTQ42API(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exp_run_poll(self):
        parameters = {
            "parameters": {
                "n": 1,
                "r": 1,
                "msg": "correct",
            },
            "inputs": {},
        }

        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm="TOY",
            version="0.1.0",
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )
        poll_result = exp_run.poll()
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, poll_result.data.status)
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, exp_run.data.status)
