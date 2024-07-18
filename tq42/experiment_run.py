from __future__ import annotations

import time
from typing import Optional, List

from google.protobuf.json_format import MessageToJson

from tq42.client import TQ42Client
from tq42.exception_handling import handle_generic_sdk_errors
from tq42.compute import HardwareProto
from tq42.algorithm import AlgorithmProto
from tq42.exceptions import ExperimentRunCancelError, ExceedRetriesError
from tq42.utils import utils

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)
from com.terraquantum.experiment.v3alpha1.experimentrun.experiment_run_pb2 import (
    ExperimentRunProto,
)
from com.terraquantum.experiment.v3alpha1.experimentrun.cancel_experiment_run_request_pb2 import (
    CancelExperimentRunRequest,
)
from com.terraquantum.experiment.v3alpha1.experimentrun.get_experiment_run_request_pb2 import (
    GetExperimentRunRequest,
)
from com.terraquantum.experiment.v3alpha1.experimentrun.list_experiment_runs_pb2 import (
    ListExperimentRunsRequest,
)
from com.terraquantum.experiment.v3alpha1.experimentrun.list_experiment_runs_pb2 import (
    ListExperimentRunsResponse,
)

from tq42.utils.pretty_list import PrettyList


class ExperimentRun:
    id: str
    client: TQ42Client
    data: ExperimentRunProto

    """
    Class to run experiments and view results
    """

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[ExperimentRunProto] = None
    ):
        self.client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get_data()

    def __repr__(self) -> str:
        return f"<ExperimentRun Id={self.id}>"

    def __str__(self) -> str:
        return f"ExperimentRun: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @handle_generic_sdk_errors
    def _get_data(self) -> ExperimentRunProto:
        """
        Gets a specific experiment run by id
        """
        get_exp_run_request = GetExperimentRunRequest(experiment_run_id=self.id)

        res = self.client.experiment_run_client.GetExperimentRun(
            request=get_exp_run_request, metadata=self.client.metadata
        )

        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: ExperimentRunProto) -> ExperimentRun:
        """
        Creates ExperimentRun instance from a protobuf message.
        """
        return ExperimentRun(client=client, id=msg.id, data=msg)

    @staticmethod
    @handle_generic_sdk_errors
    def create(
        client: TQ42Client,
        algorithm: AlgorithmProto,
        experiment_id: str,
        compute: HardwareProto,
        parameters: dict,
    ) -> ExperimentRun:
        """
        Create an experiment run.

        For details, see
        https://docs.tq42.com/en/latest/Python_Developer_Guide/Submitting_and_Monitoring_a_Run.html#submitting-an-experiment-run
        """
        create_exp_run_request = utils.dynamic_create_exp_run_request(
            parameters=parameters,
            algo=algorithm,
            exp_id=experiment_id,
            hardware=compute,
        )

        res: ExperimentRunProto = client.experiment_run_client.CreateExperimentRun(
            request=create_exp_run_request, metadata=client.metadata
        )

        client.exp_run_id = utils.get_id(res).strip().replace('"', "")
        return ExperimentRun.from_proto(client=client, msg=res)

    @handle_generic_sdk_errors
    def check(self) -> ExperimentRun:
        """
        Monitor run status.

        For details, see
        https://docs.tq42.com/en/latest/Python_Developer_Guide/Submitting_and_Monitoring_a_Run.html#monitoring-an-experiment-run
        """
        self.data = self._get_data()
        return self

    @handle_generic_sdk_errors
    def poll(
        self, tries=1000, initial_delay=1.0, delay=1.0, backoff=1.0
    ) -> ExperimentRun:
        """
        Monitor an experiment run until it completes, then automatically display the results (if there are no errors).

        For details, see
        https://docs.tq42.com/en/latest/Python_Developer_Guide/Submitting_and_Monitoring_a_Run.html#monitoring-an-experiment-run
        """
        time.sleep(initial_delay)

        for _ in range(tries):
            self.data = self._get_data()
            if self.data.status in [
                ExperimentRunStatusProto.COMPLETED,
                ExperimentRunStatusProto.CANCELLED,
                ExperimentRunStatusProto.FAILED,
            ]:
                return self

            time.sleep(delay)
            delay *= backoff

        raise ExceedRetriesError(tries=tries)

    @handle_generic_sdk_errors
    def cancel(self) -> ExperimentRun:
        """
        Cancel a run that is QUEUED, PENDING, or RUNNING.

        For details, see
        https://docs.tq42.com/en/latest/Python_Developer_Guide/Submitting_and_Monitoring_a_Run.html#cancelling-an-experiment-run
        """
        try:
            cancel_exp_runs_response = CancelExperimentRunRequest(
                experiment_run_id=self.id
            )
            self.client.experiment_run_client.CancelExperimentRun(
                request=cancel_exp_runs_response, metadata=self.client.metadata
            )
            return self
        except Exception:
            raise ExperimentRunCancelError()


@handle_generic_sdk_errors
def list_all(client: TQ42Client, experiment_id: str) -> List[ExperimentRun]:
    """
    List all the runs within an experiment you have permission to view.

    For details, see
    https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#list-all-runs-within-an-experiment
    """
    list_exp_run_request = ListExperimentRunsRequest(experiment_id=experiment_id)

    res: ListExperimentRunsResponse = client.experiment_run_client.ListExperimentRuns(
        request=list_exp_run_request, metadata=client.metadata
    )
    # TODO: It seems like currently the API returns `experiment_runs` instead of `experimentRuns` as in the protobufs
    return PrettyList(
        [
            ExperimentRun.from_proto(client=client, msg=experiment_run)
            for experiment_run in res.experiment_runs
        ]
    )
