from __future__ import annotations

from typing import List, Callable

from google.protobuf import empty_pb2

from tq42.exception_handling import handle_generic_sdk_errors
from com.terraquantum.channel.v1alpha1.create_channel_pb2 import CreateChannelResponse

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


class Channel:
    """
    Class to create and view datasets
    """

    id: str
    client: TQ42Client

    def __init__(self, client: TQ42Client, id: str):
        self.client = client
        self.id = id

    def __repr__(self) -> str:
        return f"<Channel Id={self.id}>"

    def __str__(self) -> str:
        return self.id

    @staticmethod
    @handle_generic_sdk_errors
    def create(client: TQ42Client) -> Channel:
        empty = empty_pb2.Empty()
        res: CreateChannelResponse = client.channel_client.CreateChannel(
            request=empty, metadata=client.metadata
        )
        return Channel(client=client, id=res.channel_id)

    @handle_generic_sdk_errors
    def connect(
        self,
        callback: Callable,
        finish_callback: Callable,
        timeout: int,
        max_duration_in_sec: int,
    ) -> Channel:
        self.client.channel_client.ConnectChannelCustomer()


@handle_generic_sdk_errors
def list_all(client: TQ42Client) -> List[Channel]:
    """
    List all channels for a given user.

    For details, see (TODO: update link once a new documentation URL is created)
    """
    raise NotImplementedError("This is a functionality still to come")
