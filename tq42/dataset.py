from __future__ import annotations

import base64
import hashlib
import os.path
from pathlib import Path
from typing import Optional, List
from urllib.error import HTTPError

from google.protobuf.json_format import MessageToJson
from tqdm import tqdm
import requests
import validators

from tq42.client import TQ42Client
from tq42.utils.exception_handling import handle_generic_sdk_errors

# This is important to re-export it!
from com.terraquantum.storage.v1alpha1.storage_pb2 import (
    DatasetSensitivityProto,
    StorageProto,
    StorageType,
)
from com.terraquantum.storage.v1alpha1.create_storage_from_file_pb2 import (
    CreateStorageFromFileRequest,
    CreateStorageFromFileResponse,
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

    https://docs.tq42.com/en/latest/Python_Developer_Guide/Work_with_Datasets.html
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
        sensitivity: DatasetSensitivityProto,
        file: str = None,
        url: str = None,
    ) -> Dataset:
        """
        Create a dataset for a project.

        For details, see https://docs.tq42.com/en/latest/Python_Developer_Guide/Working_with_Datasets.html
        """

        if (file and url) or (not file and not url):
            raise ValueError("Please provide (only) one of: file or url")

        if url:
            res = Dataset._create_from_external_bucket(
                client=client,
                project_id=project_id,
                name=name,
                description=description,
                url=url,
                sensitivity=sensitivity,
            )
            return Dataset.from_proto(client=client, msg=res)

        res = Dataset._create_from_file(
            client=client,
            project_id=project_id,
            name=name,
            description=description,
            file=file,
            sensitivity=sensitivity,
        )
        return Dataset.from_proto(client=client, msg=res)

    @staticmethod
    def _create_from_file(
        client: TQ42Client,
        project_id: str,
        name: str,
        description: str,
        file: str,
        sensitivity: DatasetSensitivityProto,
    ) -> StorageProto:
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError("The specified file does not exist")

        with file_path.open(mode="rb") as f:
            data = f.read()
            file_hash = hashlib.md5(data).digest()
            file_hash_b64 = base64.b64encode(file_hash).decode("utf-8")

            create_dataset_request = CreateStorageFromFileRequest(
                project_id=project_id,
                name=name,
                description=description,
                hash_md5=file_hash_b64,
                file_name=file_path.name,
                sensitivity=sensitivity,
            )

            res: CreateStorageFromFileResponse = (
                client.storage_client.CreateStorageFromFile(
                    request=create_dataset_request, metadata=client.metadata
                )
            )

            headers = {
                "Content-Type": "application/octet-stream",
                "Content-MD5": file_hash_b64,
            }
            file_upload_response = requests.put(
                url=res.signed_url,
                headers=headers,
                data=data,
            )

            if not file_upload_response.ok:
                raise HTTPError(
                    url=res.signed_url,
                    code=file_upload_response.status_code,
                    msg=f"Upload of file {file} to storage failed. Please make sure your network is working. "
                    "If issues persist please get in touch via https://help.terraquantum.io/en",
                    fp=None,
                    hdrs=file_upload_response.headers,
                )

        return res.storage

    @staticmethod
    def _create_from_external_bucket(
        client: TQ42Client,
        project_id: str,
        name: str,
        description: str,
        url: str,
        sensitivity: DatasetSensitivityProto,
    ) -> StorageProto:
        create_dataset_request = CreateStorageFromExternalBucketRequest(
            project_id=project_id,
            name=name,
            description=description,
            url=url,
            sensitivity=sensitivity,
        )

        return client.storage_client.CreateStorageFromExternalBucket(
            request=create_dataset_request, metadata=client.metadata
        )

    @handle_generic_sdk_errors
    def export(self, directory_path: str) -> List[str]:
        """
        Export all files within the dataset.
        Returns a list of exported file paths

        For details, see https://docs.tq42.com/en/latest/Python_Developer_Guide/Working_with_Datasets.html
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

    For details, see https://docs.tq42.com/en/latest/Python_Developer_Guide/Working_with_Datasets.html
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
