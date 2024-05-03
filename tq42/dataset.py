from __future__ import annotations

from typing import Optional, List

from tq42.client import TQ42Client
from tq42.exception_handling import handle_generic_sdk_errors

# This is important to re-export it!
from com.terraquantum.experiment.v1.dataset.dataset_pb2 import (
    DatasetSensitivityProto,
    DatasetProto,
)
from com.terraquantum.experiment.v1.dataset.create_dataset_request_pb2 import (
    CreateDatasetRequest,
)
from com.terraquantum.experiment.v1.dataset.list_datasets_pb2 import (
    ListDatasetsRequest,
    ListDatasetsResponse,
)


class Dataset:
    """
    Class to create and view datasets
    """

    id: str
    data: DatasetProto
    client: TQ42Client

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[DatasetProto] = None
    ):
        self.client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get()

    def __repr__(self) -> str:
        return f"<Dataset Id={self.id} Name={self.data.name}>"

    def __str__(self) -> str:
        return str(self.data)

    @handle_generic_sdk_errors
    def _get(self) -> DatasetProto:
        raise NotImplementedError(
            "there is no currently no way to get a specific dataset via the API"
        )

    @staticmethod
    def from_proto(client: TQ42Client, msg: DatasetProto) -> Dataset:
        """
        Creates Dataset instance from a protobuf message.
        """
        return Dataset(client=client, id=msg.id, data=msg)

    @staticmethod
    @handle_generic_sdk_errors
    def create(
        client: TQ42Client,
        project_id: str,
        name: str,
        description: str,
        url: str,
        sensitivity: DatasetSensitivityProto,
    ) -> Dataset:
        """
        Create a dataset for a project.

        For details, see (TODO: update link once a new documentation URL is created)
        """
        create_dataset_request = CreateDatasetRequest(
            request_id=None,
            project_id=project_id,
            name=name,
            description=description,
            url=url,
            sensitivity=sensitivity,
        )

        res: DatasetProto = client.dataset_client.CreateDataset(
            request=create_dataset_request, metadata=client.metadata
        )

        return Dataset.from_proto(client=client, msg=res)


@handle_generic_sdk_errors
def list_all(client: TQ42Client, project_id: str) -> List[Dataset]:
    """
    List all datasets for a project.

    For details, see (TODO: update link once a new documentation URL is created)
    """
    list_datasets_request = ListDatasetsRequest(project_id=project_id)
    res: ListDatasetsResponse = client.dataset_client.ListDatasets(
        request=list_datasets_request, metadata=client.metadata
    )
    return [Dataset.from_proto(client=client, msg=dataset) for dataset in res.datasets]
