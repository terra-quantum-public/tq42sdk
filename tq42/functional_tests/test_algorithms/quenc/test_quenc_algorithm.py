import unittest
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.algorithm import AlgorithmProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import ExperimentRunStatusProto
from tq42.utils.decorators import timeout


class TestQuencAlgorithm(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @timeout(240)
    def test_quenc_algorithm_successfully_runs(self):
        parameters = {
            'parameters': {
                'qubo': [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  
                'number_layers': 5,
                'steps': 25,
                'velocity': 0.05,
                'optimizer': 'ADAM'
            },
            'inputs': {}
        }

        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm=AlgorithmProto.TETRA_QUENC,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )

        self.assertEqual(self.exp, exp_run.data.experiment_id)
        self.assertEqual(ExperimentRunStatusProto.QUEUED, exp_run.data.status)

        final_status = exp_run.poll().data.status
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, final_status)
        self.assertIsNotNone(exp_run.data.result)
        self.assertIsNotNone(exp_run.data.result.tetra_qu_enc_outcome.outputs.circuit.storage_id)
        self.assertIsNotNone(exp_run.data.result.tetra_qu_enc_outcome.result)


if __name__ == '__main__':
    unittest.main()
