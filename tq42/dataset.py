from __future__ import annotations

from typing import Optional, List

from tq42.client import TQ42Client
from tq42.exception_handling import handle_generic_sdk_errors

# This is important to re-export it!
from com.terraquantum.storage.v1alpha1.storage_pb2 import (
    DatasetSensitivityProto,
    StorageProto,
    StorageType,
)
from com.terraquantum.storage.v1alpha1.create_storage_from_external_pb2 import (
    CreateStorageFromExternalBucketRequest,
)
from com.terraquantum.storage.v1alpha1.list_storages_pb2 import (
    ListStoragesRequest,
    ListStoragesResponse,
)


class Dataset:
    """
    Class to create and view datasets
    """

    id: str
    data: StorageProto
    client: TQ42Client

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[StorageProto] = None
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
    def _get(self) -> StorageProto:
        raise NotImplementedError(
            "there is no currently no way to get a specific dataset via the API"
        )

    @staticmethod
    def from_proto(client: TQ42Client, msg: StorageProto) -> Dataset:
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
        create_dataset_request = CreateStorageFromExternalBucketRequest(
            project_id=project_id,
            name=name,
            description=description,
            url=url,
            sensitivity=sensitivity,
        )

        res: StorageProto = client.storage_client.CreateStorageFromExternalBucket(
            request=create_dataset_request, metadata=client.metadata
        )

        return Dataset.from_proto(client=client, msg=res)


@handle_generic_sdk_errors
def list_all(client: TQ42Client, project_id: str) -> List[Dataset]:
    """
    List all datasets for a project.

    For details, see (TODO: update link once a new documentation URL is created)
    """
    list_datasets_request = ListStoragesRequest(
        project_id=project_id, type=StorageType.DATASET
    )
    res: ListStoragesResponse = client.storage_client.ListStorages(
        request=list_datasets_request, metadata=client.metadata
    )
    return [Dataset.from_proto(client=client, msg=dataset) for dataset in res.storages]
