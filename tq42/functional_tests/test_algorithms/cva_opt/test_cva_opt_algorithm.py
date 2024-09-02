import unittest

from google.protobuf.json_format import MessageToDict

from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)
from tq42.channel import Channel, Ask, Tell
from tq42.utils.decorators import timeout
import OptimizationTestFunctions as otf
import numpy as np
import asyncio


class TestCvaOptAlgorithm(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @timeout(240)
    def test_cva_opt_algorithm_successfully_runs(self):
        cva_params = {}
        cva_params["objectives"] = [{"name": "Rosenbrock", "aim_type": "MINIMIZE"}]
        cva_params["variables"] = []
        cva_params["variables"].append(
            {"name": "x1", "info_real": {"lower_bound": -1.0, "upper_bound": 1.0}}
        )
        cva_params["variables"].append(
            {"name": "x2", "info_real": {"lower_bound": -1.0, "upper_bound": 1.0}}
        )
        cva_params["parameters"] = {}
        cva_params["parameters"]["max_generation"] = 50
        cva_params["parameters"]["mue"] = 2
        cva_params["parameters"]["lambda"] = 10

        async def run_exp_with_channel(client, experiment_id, cva_params):
            channel = await Channel.create(client=client)
            # extend cva_params with func_eval_worker_channel_id
            cva_params["func_eval_worker_channel_id"] = channel.id

            # create the experiment run
            run = ExperimentRun.create(
                client=client,
                algorithm="CVA_OPT",
                version="0.1.0",
                experiment_id=experiment_id,
                compute=HardwareProto.SMALL,
                parameters={"parameters": cva_params, "inputs": {}},
            )

            # define the callback function
            async def callback(ask: Ask) -> Tell:
                dim = len(ask.headers)
                func = otf.Rosenbrock(dim)
                y = []
                for parameter in ask.parameters:
                    y.append(float(func(np.array(parameter.values))))
                # add result to data

                return Tell(parameters=ask.parameters, headers=ask.headers, results=y)

            # define a function to be called after the optimization is finished
            def success():
                pass

            # let the channel wait for connections
            is_finished = False
            max_retries = 10
            retries = 0
            while (not is_finished) and (retries < max_retries):
                await channel.connect(
                    callback=callback,
                    finish_callback=success,
                    max_duration_in_sec=None,
                    message_timeout_in_sec=240,
                )
                retries += 1
                run_state = run.check().data.status
                if ExperimentRunStatusProto.Name(run_state) in [
                    "CANCELLED",
                    "COMPLETED",
                    "FAILED",
                    "CANCEL_PENDING",
                ]:
                    is_finished = True
            # return the run to retrieve the result
            return run

        loop = asyncio.get_event_loop()
        run = loop.run_until_complete(
            run_exp_with_channel(self.get_client(), self.exp, cva_params)
        )
        run_result = run.poll()
        self.assertEqual(ExperimentRunStatusProto.COMPLETED, run_result.data.status)
        self.assertIsNotNone(run_result.data.result)
        outcome = MessageToDict(run_result.data.result.outcome)
        self.assertIsNotNone(eval(outcome["result"])["result"]["x1"])


if __name__ == "__main__":
    unittest.main()
