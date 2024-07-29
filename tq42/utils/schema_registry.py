import logging
import os
from typing import Dict, Type, Optional

import grpc
from buf.reflect.v1beta1.file_descriptor_set_pb2 import (
    GetFileDescriptorSetResponse,
    GetFileDescriptorSetRequest,
)
from buf.reflect.v1beta1.file_descriptor_set_pb2_grpc import (
    FileDescriptorSetServiceStub,
)
from google.protobuf import message_factory
from google.protobuf.message import Message

_REGISTRY_HOST = os.getenv("TQ42_SCHEMA_REGISTRY_HOST ", "buf.build")
_REGISTRY_ACCOUNT = os.getenv("TQ42_SCHEMA_REGISTRY_ACCOUNT", "tq42-algorithms")


def get_metadata_proto(algorithm: str, version: str) -> Optional[Type[Message]]:
    messages = _get_message_types(algorithm=algorithm, version=version)

    protos = [
        message_type
        for name, message_type in messages.items()
        if name.endswith("MetadataProto")
    ]
    if len(protos) == 0:
        return None
    elif len(protos) > 1:
        logging.warning(
            f"Found multiple matching metadata types for {algorithm=}, using the first one: {[proto.__name__ for proto in protos]}"
        )

    return protos[0]


def _get_message_types(algorithm: str, version: str) -> Dict[str, Type[Message]]:
    with grpc.secure_channel(
        _REGISTRY_HOST, credentials=grpc.ssl_channel_credentials()
    ) as channel:
        service = FileDescriptorSetServiceStub(channel=channel)

        result: GetFileDescriptorSetResponse = service.GetFileDescriptorSet(
            request=GetFileDescriptorSetRequest(
                module=f"{_REGISTRY_HOST}/{_REGISTRY_ACCOUNT}/{_algorithm_to_repository_name(algorithm)}",
                version=version,
            ),
        )

        return message_factory.GetMessages(file_protos=result.file_descriptor_set.file)


def _algorithm_to_repository_name(algorithm: str) -> str:
    """
    convert from SOME_ALGORITHM_NAME to some-algorithm-name
    """
    return algorithm.replace("_", "-").lower()
