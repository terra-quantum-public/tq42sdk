import OptimizationTestFunctions as otf
import numpy as np
from pytest import mark, fixture

from tq42.channel import Channel, Ask, Tell
from tq42.experiment_run import ExperimentRun
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)


@fixture
def functional_test_config():
    return FunctionalTestConfig()


@mark.asyncio
async def test_channel_create(functional_test_config):
    channel = await Channel.create(client=functional_test_config.get_client())
    assert channel.id is not None


@mark.asyncio
async def test_exp_run_with_channel(functional_test_config):
    channel = await Channel.create(client=functional_test_config.get_client())
    cva_params = {
        "objectives": [{"name": "Ackley", "aim_type": "MINIMIZE"}],
        "variables": [
            {"name": "x1", "info_real": {"lower_bound": -1.0, "upper_bound": 1.0}},
            {"name": "x2", "info_real": {"lower_bound": -1.0, "upper_bound": 1.0}},
        ],
        "func_eval_worker_channel_id": channel.id,
        "parameters": {"max_generation": 3, "mue": 15, "lambda": 100},
    }

    exp_run = ExperimentRun.create(
        client=functional_test_config.get_client(),
        algorithm=AlgorithmProto.CVA_OPT,
        experiment_id=functional_test_config.exp,
        compute=HardwareProto.SMALL,
        parameters={"parameters": cva_params, "inputs": {}},
    )

    async def callback(ask: Ask) -> Tell:
        dim = len(ask.headers)
        func = otf.Ackley(dim)
        y = []
        for parameter in ask.parameters:
            y.append(float(func(np.array(parameter.values))))

        return Tell(parameters=ask.parameters, headers=ask.headers, results=y)

    def success():
        poll_result = exp_run.poll()
        assert ExperimentRunStatusProto.COMPLETED == poll_result.data.status

    await channel.connect(
        callback=callback,
        finish_callback=success,
        max_duration_in_sec=None,
        message_timeout_in_sec=300,
    )

    assert exp_run.data.status == ExperimentRunStatusProto.COMPLETED
