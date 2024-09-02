import unittest
from google.protobuf.json_format import MessageToDict
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.algorithm import AlgorithmProto, ToyMetadataProto, ToyParametersProto, ToyInputsProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import ExperimentRunStatusProto
from tq42.utils.decorators import timeout


class TestToyAlgorithm(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @timeout(180)
    def test_toy_algorithm_successfully_runs(self):
        parameters = ToyMetadataProto(
            parameters=ToyParametersProto(n=2, r=1, msg="Toy algorithm test"),
            inputs=ToyInputsProto(),
        )
        parameters = MessageToDict(
            parameters, preserving_proto_field_name=True)

        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm=AlgorithmProto.TOY,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )

        self.assertEqual(self.exp, exp_run.data.experiment_id)
        self.assertEqual(ExperimentRunStatusProto.QUEUED, exp_run.data.status)

        final_status = exp_run.poll().data.status
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, final_status)
        self.assertIsNotNone(exp_run.data.result)

    @timeout(180)
    def test_toy_algorithm_fails_with_wrong_message(self):
        parameters = ToyMetadataProto(
            parameters=ToyParametersProto(n=2, r=1, msg="wrong"),
            inputs=ToyInputsProto(),
        )
        parameters = MessageToDict(
            parameters, preserving_proto_field_name=True)

        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm=AlgorithmProto.TOY,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )

        self.assertEqual(self.exp, exp_run.data.experiment_id)
        self.assertEqual(ExperimentRunStatusProto.QUEUED, exp_run.data.status)

        final_status = exp_run.poll().data.status
        self.assertEqual(ExperimentRunStatusProto.FAILED, final_status)
        self.assertIsNotNone(exp_run.data.error_message)
        self.assertEqual(
            exp_run.data.error_message,
            '{"error": "That\'s wrong!"}'
        )


if __name__ == '__main__':
    unittest.main()
