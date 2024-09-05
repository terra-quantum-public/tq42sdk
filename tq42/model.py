from __future__ import annotations

from typing import Optional, List

from google.protobuf.json_format import MessageToJson

from tq42.client import TQ42Client
from tq42.utils.exception_handling import handle_generic_sdk_errors

from com.terraquantum.storage.v1alpha1.storage_pb2 import (
    StorageProto,
    StorageType,
)
from com.terraquantum.storage.v1alpha1.get_storage_request_pb2 import GetStorageRequest
from com.terraquantum.storage.v1alpha1.list_storages_pb2 import (
    ListStoragesRequest,
    ListStoragesResponse,
)

from tq42.utils.pretty_list import PrettyList


class Model:
    """
    Reference an existing model.

    :param client: a client instance
    :param id: the id of the existing model
    :param data: only used internally
    """

    id: str
    """ID of the model"""
    data: StorageProto
    """Object containing all attributes of the model"""
    _client: TQ42Client

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[StorageProto] = None
    ):
        self._client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get()

    def __repr__(self) -> str:
        return f"<Model Id={self.id} Name={self.data.name}>"

    def __str__(self) -> str:
        return f"Model: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @handle_generic_sdk_errors
    def _get(self) -> StorageProto:
        get_storage_request = GetStorageRequest(storage_id=self.id)
        storage_data: StorageProto = self._client.storage_client.GetStorage(
            request=get_storage_request, metadata=self._client.metadata
        )
        return storage_data

    def _refresh(self) -> None:
        self.data = self._get()

    @staticmethod
    def from_proto(client: TQ42Client, msg: StorageProto) -> Model:
        """
        Creates model instance from a protobuf message.

        :meta private:
        """
        return Model(client=client, id=msg.id, data=msg)


@handle_generic_sdk_errors
def list_all(client: TQ42Client, project_id: str) -> List[Model]:
    """
    List all models for a project.

    :param client: a client instance
    :param project_id: the id of a project
    """
    list_models_request = ListStoragesRequest(
        project_id=project_id, type=StorageType.MODEL
    )
    res: ListStoragesResponse = client.storage_client.ListStorages(
        request=list_models_request, metadata=client.metadata
    )
    return PrettyList(
        [Model.from_proto(client=client, msg=model) for model in res.storages]
    )
