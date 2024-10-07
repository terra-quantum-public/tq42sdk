import asyncio
from typing import Awaitable

import numpy as np
import pytest
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)

from tq42.channel import Ask, Tell, Channel
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
import OptimizationTestFunctions as otf
from scipy import optimize

from tq42.utils.decorators import timeout


@pytest.fixture
def config() -> FunctionalTestConfig:
    return FunctionalTestConfig()


@pytest.fixture
async def channels(config) -> tuple[Channel, Channel]:
    client = config.get_client()
    objective_func_channel = await Channel.create(client=client)
    local_opt_channel = await Channel.create(client=client)
    return objective_func_channel, local_opt_channel


@timeout(240)
@pytest.mark.asyncio
async def test_tetra_opt_successfully_runs(
    config: FunctionalTestConfig, channels: Awaitable[tuple[Channel, Channel]]
):
    objective_func_channel, local_opt_channel = await channels
    tetra_opt_params = {
        "dimensionality": 4,
        "iteration_number": 2,
        "maximal_rank": 4,
        "points_number": 1,
        "quantization": False,
        "tolerance": 0.001,
        "lower_limits": [0, 0, 0, 0],
        "upper_limits": [9, 9, 9, 9],
        "grid": [10, 10, 10, 10],
        "objective_function_channel_id": objective_func_channel.id,
        "local_optimizer_channel_id": local_opt_channel.id,
    }

    run = ExperimentRun.create(
        client=config.get_client(),
        algorithm="TETRA_OPT",
        version="0.3.2",
        experiment_id=config.exp,
        compute=HardwareProto.SMALL,
        parameters={"parameters": tetra_opt_params, "inputs": {}},
    )

    assert config.exp == run.data.experiment_id
    assert ExperimentRunStatusProto.QUEUED == run.data.status

    def discard():
        pass

    await asyncio.gather(
        objective_func_channel.connect(
            callback=objective_function_callback,
            finish_callback=discard,
            max_duration_in_sec=None,
            message_timeout_in_sec=500,
        ),
        local_opt_channel.connect(
            callback=local_optimization_function_callback,
            finish_callback=discard,
            max_duration_in_sec=None,
            message_timeout_in_sec=500,
        ),
    )

    run.poll()

    assert ExperimentRunStatusProto.COMPLETED == run.data.status
    assert run.result is not None

    assert isinstance(run.result.get("x"), list), "Expected 'x' to be a list"
    assert all(
        isinstance(x, float) for x in run.result.get("x")
    ), "Expected 'x' to be a list of floats"
    assert isinstance(run.result.get("y"), list), "Expected 'y' to be a list"
    assert all(
        isinstance(y, float) for y in run.result.get("y")
    ), "Expected 'y' to be a list of floats"


async def objective_function_callback(ask: Ask) -> Tell:
    dim = len(ask.headers)
    func = otf.Ackley(dim)
    y = [float(func(np.array(parameter.values))) for parameter in ask.parameters]

    tell = Tell(parameters=ask.parameters, headers=ask.headers, results=y)
    return tell


async def local_optimization_function_callback(ask: Ask) -> Tell:
    dim = len(ask.headers)
    func = otf.Ackley(dim)
    results, new_x = [], []

    for parameter in ask.parameters:
        res = optimize.minimize(func, np.array(parameter.values))
        new_x.append({"values": res.x})
        results.append(float(res.fun))

    tell = Tell(
        parameters=ask.parameters,
        headers=ask.headers,
        results=results,
        candidates=new_x,
    )
    return tell
