import asyncio
import json
from typing import Awaitable

import pandas as pd
import pytest
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)

from tq42.channel import Ask, Tell, Channel
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.utils.decorators import timeout


def _mass_flow_lm(row):
    return (
        0.019745030906364664
        + 0.00013074793399258446 * row["alpha"]
        + 0.0004949044385859217 * row["beta"]
        + 0.04551741292831213 * row["d2"]
        + 0.0007926550728449819 * row["l1"]
        + 0.000271121128077387 * row["l3"] * -5.9455600147173825e-05 * row["l4"]
    )


def _tumble_lm(row):
    return (
        2.8951535034749316
        + -0.013713771116343086 * row["alpha"]
        + -0.040331795422272596 * row["beta"]
        + -0.004121931530295305 * row["d1"]
        + -1.0597227166208407 * row["d2"]
        + -0.03846219537291295 * row["l1"]
        + 0.00020282278982582672 * row["l2"]
        + -0.008908198543821947 * row["l3"]
        + 0.003848225284017235 * row["l4"]
    )


@pytest.fixture
def config() -> FunctionalTestConfig:
    return FunctionalTestConfig()


@pytest.fixture
async def channels(config) -> tuple[Channel, Channel]:
    client = config.get_client()
    mass_flow_channel = await Channel.create(client=client)
    tumble_channel = await Channel.create(client=client)
    return mass_flow_channel, tumble_channel


@timeout(240)
@pytest.mark.asyncio
async def test_optimax_successfully_runs(
    config: FunctionalTestConfig, channels: Awaitable[tuple[Channel, Channel]]
):
    mass_flow_channel, tumble_channel = await channels
    optimax_params = {
        "variable_names": ["alpha", "beta", "d1", "d2", "l1", "l2", "l3", "l4"],
        "variable_lb": [52.0, 20.0, 0.5, 0.4, 0.0, 10.0, 0.0, 75.0],
        "variable_ub": [56.0, 30.0, 5.0, 0.9, 7.0, 45.0, 25.0, 95.0],
        "objective_names": ["mass_flow", "tumble"],
        "objective_aims": ["maximize", "maximize"],
        "reference_point": [0.0, 0.0],
        "func_eval_worker_channel_ids": [
            mass_flow_channel.id,
            tumble_channel.id,
        ],
        "max_generation": 1,
        "pf_opt_lambda": 2,
        "hv_opt_repetition": 1,
        "tq_hv_opt_iterations": 3,
        "tq_hv_opt_max_rank": 2,
        "tq_hv_opt_grid": 32,
    }

    run = ExperimentRun.create(
        client=config.get_client(),
        algorithm="OPTIMAX",
        version="0.0.3",
        experiment_id=config.exp,
        compute=HardwareProto.SMALL,
        parameters={
            "parameters": {"parameter_string": json.dumps(optimax_params)},
            "inputs": {},
        },
    )

    assert config.exp == run.data.experiment_id
    assert ExperimentRunStatusProto.QUEUED == run.data.status

    def discard():
        pass

    await asyncio.gather(
        mass_flow_channel.connect(
            callback=_mass_flow_callback,
            finish_callback=discard,
            max_duration_in_sec=None,
            message_timeout_in_sec=1200,
        ),
        tumble_channel.connect(
            callback=_tumble_callback,
            finish_callback=discard,
            max_duration_in_sec=None,
            message_timeout_in_sec=1200,
        ),
    )

    run.poll()

    assert ExperimentRunStatusProto.COMPLETED == run.data.status
    assert run.result is not None

    assert "mass_flow" in run.result
    assert "tumble" in run.result


async def _mass_flow_callback(ask: Ask) -> Tell:
    mass_flow = []
    for parameter in ask.parameters:
        row = pd.Series()
        for i, variable_name in enumerate(ask.headers):
            row[variable_name] = parameter.values[i]
        mass_flow.append(float(_mass_flow_lm(row)))
    return Tell(parameters=ask.parameters, headers=ask.headers, results=mass_flow)


async def _tumble_callback(ask: Ask) -> Tell:
    tumble = []
    for parameter in ask.parameters:
        row = pd.Series()
        for i, variable_name in enumerate(ask.headers):
            row[variable_name] = parameter.values[i]
        tumble.append(float(_tumble_lm(row)))
    return Tell(parameters=ask.parameters, headers=ask.headers, results=tumble)
