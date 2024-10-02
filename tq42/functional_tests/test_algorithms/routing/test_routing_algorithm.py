import json
import os.path
import uuid

import pytest
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)
from com.terraquantum.storage.v1alpha1.storage_pb2 import DatasetSensitivityProto

from tq42.dataset import Dataset
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.utils.decorators import timeout


@pytest.fixture
def config() -> FunctionalTestConfig:
    return FunctionalTestConfig()


@pytest.fixture
def data_storage_id(config: FunctionalTestConfig) -> str:
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    dataset = Dataset.create(
        client=config.get_client(),
        project_id=config.proj,
        name=str(uuid.uuid4()),
        description="Test dataset",
        sensitivity=DatasetSensitivityProto.SENSITIVE,
        file=data_path,
    )
    return dataset.id


@timeout(240)
def test_routing_successfully_runs(config: FunctionalTestConfig, data_storage_id: str):
    routing_params = {
        "nbGranular": 20,
        "mu": 25,
        "lambda": 40,
        "nbElite": 4,
        "nbClose": 5,
        "nbIterPenaltyManagement": 1000,
        "targetFeasible": 0.2,
        "seed": -1,
        "nbIter": 40000,
        "nbIterImpr": 25000,
        "nbIterTraces": 500,
        "timeOutput": 0.5,
        "timeLimit": 30,
        "penalty_cap": 3,
        "penalty_tw": 30,
        "penalty_dur": 20,
        "n_vehicles": 0,
        "round": 2,
    }

    run = ExperimentRun.create(
        client=config.get_client(),
        algorithm="ROUTING",
        version="0.1.4",
        experiment_id=config.exp,
        compute=HardwareProto.SMALL,
        parameters={
            "parameters": {"parameter_string": json.dumps(routing_params)},
            "inputs": {"data": {"storage_id": data_storage_id}},
        },
    )

    assert config.exp == run.data.experiment_id
    assert ExperimentRunStatusProto.QUEUED == run.data.status

    run.poll()

    assert ExperimentRunStatusProto.COMPLETED == run.data.status
    assert run.outputs is not None
    assert "solution" in run.outputs
    assert run.outputs.get("solution").get("storage_id") is not None
