import unittest
from pytest import mark

from google.protobuf.json_format import MessageToDict

from tq42.experiment_run import ExperimentRun
from tq42.functional_tests.functional_test_config import FunctionalTestConfig

from tq42.algorithm import ToyMetadataProto, ToyParametersProto, ToyInputsProto
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
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
        parameters = ToyMetadataProto(
            parameters=ToyParametersProto(n=2, r=1, msg="correct"),
            inputs=ToyInputsProto(),
        )
        parameters = MessageToDict(parameters, preserving_proto_field_name=True)

        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm=AlgorithmProto.TOY,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )
        poll_result = exp_run.poll()
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, poll_result.data.status)
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, exp_run.data.status)
