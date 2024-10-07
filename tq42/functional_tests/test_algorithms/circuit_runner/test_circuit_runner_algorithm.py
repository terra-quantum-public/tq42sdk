import pytest
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)

from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.utils.decorators import timeout


@pytest.fixture
def config():
    return FunctionalTestConfig()


@timeout(240)
@pytest.fixture
def circuit_storage_id(config):
    parameters = {
        "parameters": {
            "qubo": [
                0,
                1,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                0,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0,
            ],
            "number_layers": 5,
            "steps": 25,
            "velocity": 0.05,
            "optimizer": "ADAM",
        },
        "inputs": {},
    }
    exp_run = ExperimentRun.create(
        client=config.get_client(),
        algorithm="QUENC",
        version="0.4.0",
        experiment_id=config.exp,
        compute=HardwareProto.SMALL,
        parameters=parameters,
    )

    return exp_run.poll().outputs.get("circuit").get("storage_id")


@timeout(240)
def test_circuit_runner_successfully_runs(config, circuit_storage_id):
    parameters = {
        "parameters": {"shots": 500, "backend": "CIRQ_SIMULATOR"},
        "inputs": {"circuit": {"storage_id": circuit_storage_id}},
    }

    run = ExperimentRun.create(
        client=config.get_client(),
        algorithm="CIRCUIT_RUN",
        version="0.2.0",
        experiment_id=config.exp,
        compute=HardwareProto.SMALL,
        parameters=parameters,
    )

    assert config.exp == run.data.experiment_id
    assert ExperimentRunStatusProto.QUEUED == run.data.status

    run.poll()

    assert ExperimentRunStatusProto.COMPLETED == run.data.status
    assert run.result is not None
