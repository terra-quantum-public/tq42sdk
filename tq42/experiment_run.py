from __future__ import annotations

import json
import time
from typing import Optional, List, Mapping, Any, Union

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)

# important for re-export
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    HardwareProto,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.cancel_experiment_run_request_pb2 import (
    CancelExperimentRunRequest,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.create_experiment_run_request_pb2 import (
    CreateExperimentRunRequest,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.experiment_run_pb2 import (
    ExperimentRunProto,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.get_experiment_run_request_pb2 import (
    GetExperimentRunRequest,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.list_experiment_runs_pb2 import (
    ListExperimentRunsRequest,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.list_experiment_runs_pb2 import (
    ListExperimentRunsResponse,
)
from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToJson, ParseDict, MessageToDict

from tq42.client import TQ42Client
from tq42.utils.exception_handling import handle_generic_sdk_errors
from tq42.exceptions import ExperimentRunCancelError, ExceedRetriesError
from tq42.utils.pretty_list import PrettyList


class ExperimentRun:
    """
    Reference an existing experiment run.

    :param client: a client instance
    :param id: the id of the existing experiment run
    :param data: only used internally
    """

    _client: TQ42Client
    id: str
    """ID of the experiment run"""
    data: ExperimentRunProto
    """Object containing all attributes of the experiment run"""

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[ExperimentRunProto] = None
    ):
        self._client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get_data()

    def __repr__(self) -> str:
        return f"<ExperimentRun Id={self.id}>"

    def __str__(self) -> str:
        return f"ExperimentRun: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @property
    def completed(self) -> bool:
        """
        Check if the experiment run is completed

        :returns: true if the experiment run is in the state `COMPLETED`
        """

        return self.data.status == ExperimentRunStatusProto.COMPLETED

    @property
    def result(self) -> Optional[dict[str, Any]]:
        """
        Get the result of the experiment run if the run is completed.

        If the result contains a results_string or if the result is a string, it will be parsed and returned.

        :returns: a dict with the result of the experiment run. If the run is not completed yet, returns `None`.
        """

        if not self.completed:
            return None

        result: Union[dict[str, Any], str] = MessageToDict(
            self.data.result.outcome
        ).get("result", {})
        if isinstance(result, str):
            return json.loads(result)
        elif "results_string" in result:
            return json.loads(result.get("results_string"))

        return result

    @property
    def outputs(self) -> Optional[dict[str, Any]]:
        """
        Get the outputs of the experiment run if the run is completed.

        :returns: a dict with the outputs of the experiment run. If the run is not completed yet, returns `None`.
        """

        if not self.completed:
            return None

        return MessageToDict(self.data.result.outcome).get("outputs", {})

    @handle_generic_sdk_errors
    def _get_data(self) -> ExperimentRunProto:
        """
        Gets a specific experiment run by id
        """
        get_exp_run_request = GetExperimentRunRequest(experiment_run_id=self.id)

        res = self._client.experiment_run_client.GetExperimentRun(
            request=get_exp_run_request, metadata=self._client.metadata
        )

        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: ExperimentRunProto) -> ExperimentRun:
        """
        Creates ExperimentRun instance from a protobuf message.

        :meta private:
        """
        return ExperimentRun(client=client, id=msg.id, data=msg)

    @staticmethod
    @handle_generic_sdk_errors
    def create(
        client: TQ42Client,
        algorithm: str,
        version: str,
        experiment_id: str,
        compute: HardwareProto,
        parameters: Mapping[str, Any],
    ) -> ExperimentRun:
        """
        Start a new experiment run in an experiment

        :param client: a client instance
        :param algorithm: name of the algorithm (e.g. `'TOY'`)
        :param version: version of the algorithm in the format `x.y.z`
        :param experiment_id: id of the experiment in which the run should be started
        :param compute: the hardware specification on which the run should be started (e.g. `HardwareProto.SMALL`)
        :param parameters: dict with parameters for the algorithm
        :returns: the created experiment run

        """

        request = CreateExperimentRunRequest(
            experiment_id=experiment_id,
            algorithm=algorithm,
            version=version,
            hardware=compute,
            metadata=ParseDict(parameters, struct_pb2.Struct()),
        )

        res: ExperimentRunProto = client.experiment_run_client.CreateExperimentRun(
            request=request, metadata=client.metadata
        )

        return ExperimentRun.from_proto(client=client, msg=res)

    @handle_generic_sdk_errors
    def check(self) -> ExperimentRun:
        """
        Update the state of the experiment run

        :returns: the updated experiment run
        """
        self.data = self._get_data()
        return self

    @handle_generic_sdk_errors
    def poll(
        self, tries=1000, initial_delay=1.0, delay=1.0, backoff=1.0
    ) -> ExperimentRun:
        """
        Monitor an experiment run until it completes, then automatically display the results (if there are no errors).

        :param tries: how many retries until the poll loop is cancelled (default: 1000)
        :param initial_delay: initial delay before starting poll loop (default: 1 second)
        :param delay: initial delay between retries (default: 1 second)
        :param backoff: backoff factor between retries (default: 1)
        :returns: the finished experiment run
        :raises: ExceedRetriesError if `tries` are exceeded
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

        :returns: the cancelled experiment run
        :raises: ExperimentRunCancelError if the experiment run is not queued, pending or running
        """
        try:
            cancel_exp_runs_response = CancelExperimentRunRequest(
                experiment_run_id=self.id
            )
            self._client.experiment_run_client.CancelExperimentRun(
                request=cancel_exp_runs_response, metadata=self._client.metadata
            )
            return self
        except Exception:
            raise ExperimentRunCancelError()


@handle_generic_sdk_errors
def list_all(client: TQ42Client, experiment_id: str) -> List[ExperimentRun]:
    """
    List all the runs within an experiment you have permission to view.

    :param client: a client instance
    :param experiment_id: id of the experiment
    :returns: a list of experiment runs
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
