from __future__ import annotations

import multiprocessing
import queue
from typing import List, Callable, Iterator

from google.protobuf import empty_pb2

from tq42.exception_handling import handle_generic_sdk_errors
from com.terraquantum.channel.v1alpha1.create_channel_pb2 import CreateChannelResponse
from com.terraquantum.channel.v1alpha1.channel_message_pb2 import ChannelMessage

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
        callback: Callable[[ChannelMessage], ChannelMessage],
        finish_callback: Callable,
        max_duration_in_sec: int,
    ) -> None:
        # Start listener as a process
        listen_process = multiprocessing.Process(
            target=self._listen_stream, args=(callback,)
        )
        listen_process.start()
        listen_process.join(max_duration_in_sec)

        # If thread is active
        if listen_process.is_alive():
            print(
                "Listen process is still running and exceeded the max_duration_in_sec timeout, killing..."
            )
            # Terminate process
            listen_process.terminate()
            listen_process.join()

        finish_callback()

    def _listen_stream(
        self, callback: Callable[[ChannelMessage], ChannelMessage]
    ) -> None:
        incoming_messages = queue.Queue()

        # establish the connection
        response_stream = self.client.channel_client.ConnectChannelCustomer(
            self._handle_messages(
                incoming_msg_queue=incoming_messages, callback=callback
            )
        )
        for msg in response_stream:
            incoming_messages.put(msg)

    @staticmethod
    def _handle_messages(
        incoming_msg_queue: queue.Queue,
        callback: Callable[[ChannelMessage], ChannelMessage],
    ) -> Iterator[ChannelMessage]:
        while True:
            incoming_msg: ChannelMessage = incoming_msg_queue.get()
            outgoing_msg: ChannelMessage = callback(incoming_msg)
            incoming_msg_queue.task_done()
            yield outgoing_msg


@handle_generic_sdk_errors
def list_all(client: TQ42Client) -> List[Channel]:
    """
    List all channels for a given user.

    For details, see (TODO: update link once a new documentation URL is created)
    """
    raise NotImplementedError("This is a functionality still to come")
