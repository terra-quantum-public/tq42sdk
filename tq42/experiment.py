from __future__ import annotations

from typing import Optional, List

from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.json_format import MessageToJson

from tq42.client import TQ42Client
from tq42.exception_handling import handle_generic_sdk_errors

from com.terraquantum.experiment.v3alpha1.experiment.experiment_pb2 import (
    ExperimentProto,
)
from com.terraquantum.experiment.v3alpha1.experiment.get_experiment_pb2 import (
    GetExperimentRequest,
)
from com.terraquantum.experiment.v3alpha1.experiment.list_experiments_pb2 import (
    ListExperimentsRequest,
)
from com.terraquantum.experiment.v3alpha1.experiment.list_experiments_pb2 import (
    ListExperimentsResponse,
)
from com.terraquantum.experiment.v3alpha1.experiment.update_experiment_request_pb2 import (
    UpdateExperimentRequest,
)

from tq42.utils.pretty_list import PrettyList
from tq42.utils.utils_for_cache import get_current_value


class Experiment:
    """
    Class to manage experiments
    """

    _client: TQ42Client
    id: str
    data: ExperimentProto

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[ExperimentProto] = None
    ):
        """
        Instantiates an experiment.
        If data is omitted the id is used to get the corresponding data from the API (used like a GET on this id)
        """
        self._client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get_data()

    def __repr__(self) -> str:
        return f"<Experiment Id={self.id} Name={self.data.name}>"

    def __str__(self) -> str:
        return (
            f"Experiment: {MessageToJson(self.data, preserving_proto_field_name=True)}"
        )

    @handle_generic_sdk_errors
    def _get_data(self) -> ExperimentProto:
        """
        Gets the data corresponding to this experiment id.
        """
        get_exp_request = GetExperimentRequest(id=self.id)
        res = self._client.experiment_client.GetExperiment(
            request=get_exp_request, metadata=self._client.metadata
        )
        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: ExperimentProto) -> Experiment:
        """
        Creates Experiment instance from a protobuf message.
        """
        return Experiment(client=client, id=msg.id, data=msg)

    @handle_generic_sdk_errors
    def update(self, name: str) -> Experiment:
        """
        Updates this specific experiment
        """
        # Create a new FieldMask instance
        field_mask = FieldMask()

        # Add paths to the FieldMask
        field_mask.paths.append("id")
        field_mask.paths.append("name")

        update_proj_request = UpdateExperimentRequest(
            update_mask=field_mask, id=self.id, name=name
        )
        self.data = self._client.experiment_client.UpdateExperiment(
            request=update_proj_request, metadata=self._client.metadata
        )

        return self

    @handle_generic_sdk_errors
    def set_friendly_name(self, friendly_name: str) -> Experiment:
        """
        Set a friendly name for an experiment.

        For details, see https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#setting-friendly-names-for-projects-and-experiments
        """
        return self.update(name=friendly_name)


@handle_generic_sdk_errors
def list_all(client: TQ42Client, project_id: Optional[str] = None) -> List[Experiment]:
    """
    List all the experiments you have permission to view within a specific project.
    If no project_id is specified the currently set project id will be used for this.

    For details, see https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#list-all-experiments
    """
    if not project_id:
        project_id = get_current_value("proj")

    list_experiments_request = ListExperimentsRequest(project_id=project_id)
    res: ListExperimentsResponse = client.experiment_client.ListExperiments(
        request=list_experiments_request, metadata=client.metadata
    )
    return PrettyList(
        [
            Experiment.from_proto(client=client, msg=experiment_run)
            for experiment_run in res.experiments
        ]
    )
