from __future__ import annotations

import os.path
from typing import Optional, List

from google.protobuf.json_format import MessageToJson
from tqdm import tqdm
import requests
import validators

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
from com.terraquantum.storage.v1alpha1.get_storage_request_pb2 import GetStorageRequest
from com.terraquantum.storage.v1alpha1.list_storages_pb2 import (
    ListStoragesRequest,
    ListStoragesResponse,
)
from com.terraquantum.storage.v1alpha1.export_storage_pb2 import (
    ExportStorageRequest,
    ExportStorageResponse,
)

from tq42.utils.pretty_list import PrettyList


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
        return f"Dataset: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @handle_generic_sdk_errors
    def _get(self) -> StorageProto:
        get_storage_request = GetStorageRequest(storage_id=self.id)
        storage_data: StorageProto = self.client.storage_client.GetStorage(
            request=get_storage_request, metadata=self.client.metadata
        )
        return storage_data

    def _refresh(self) -> None:
        self.data = self._get()

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
    def export(self, directory_path: str) -> List[str]:
        """
        Export all files within the dataset.
        Returns a list of exported file paths
        """
        if not os.path.isdir(directory_path):
            raise ValueError(
                f"Provided directory path {directory_path} is not a valid directory"
            )

        export_storage_request = ExportStorageRequest(storage_id=self.id)

        res: ExportStorageResponse = self.client.storage_client.ExportStorage(
            request=export_storage_request, metadata=self.client.metadata
        )

        exported_file_paths = []

        for signed_url in res.signed_urls:
            file_path = os.path.join(
                directory_path,
                self._get_file_name_from_signed_url(signed_url=signed_url),
            )
            self._download_file_from_url(url=signed_url, file_path=file_path)
            exported_file_paths.append(file_path)

        return exported_file_paths

    @staticmethod
    def _download_file_from_url(url: str, file_path: str):
        response = requests.get(url, stream=True)

        if os.path.exists(file_path):
            raise FileExistsError(file_path)

        print("Downloading file to {}".format(file_path))
        with open(file_path, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

    @staticmethod
    def _get_file_name_from_signed_url(signed_url: str) -> str:
        if not validators.url(signed_url):
            raise ValueError(f"The signed URL {signed_url} is not a valid URL")
        url_without_parameters = signed_url.split("?")[0]
        return url_without_parameters.split("/")[-1]


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
    return PrettyList(
        [Dataset.from_proto(client=client, msg=dataset) for dataset in res.storages]
    )
