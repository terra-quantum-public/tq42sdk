from __future__ import annotations

import asyncio
import queue
import time
from datetime import datetime
from typing import List, Callable, Iterator

from google.protobuf import empty_pb2

from tq42.exception_handling import handle_generic_sdk_errors
from com.terraquantum.channel.v1alpha1.create_channel_pb2 import CreateChannelResponse

# important for re-export
from com.terraquantum.channel.v1alpha1.channel_message_pb2 import (
    ChannelMessage,
    Ask,
    Parameter,
)

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

    def connect_algo(
        self,
        callback: Callable[[ChannelMessage], ChannelMessage],
        finish_callback: Callable,
        max_duration_in_sec: int = 0,
    ) -> None:
        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            self.handle_algo(callback=callback, max_duration_in_sec=max_duration_in_sec)
        )

        loop.close()
        finish_callback()

    async def handle_algo(
        self,
        callback: Callable[[ChannelMessage], ChannelMessage],
        max_duration_in_sec: int = 0,
    ):
        # establish the connection
        print("starting")
        metadata: tuple = (
            *self.client.metadata,
            ("channel-id", self.id),
        )
        print(metadata)
        call = self.client.channel_client.ConnectChannelAlgorithm(metadata=metadata)

        print("writing channel message")
        msg = ChannelMessage()
        print("sending this msg", msg)
        await call.write(msg)
        print("writing channel message done")

        timeout_start = time.time()

        while time.time() < timeout_start + max_duration_in_sec:
            print("Waiting for message")
            ask = ChannelMessage(
                sequential_message_id=1,
                ask_data=Ask(
                    parameters=[Parameter(values=[0, 1, 2])], headers=["h1", "h2", "h3"]
                ),
            )
            ask.timestamp.FromDatetime(datetime.now())
            await call.write(ask)
            print("Send message, now waiting for response")
            response = await call.read()
            print("Response", response)

        await call.done_writing()

    def connect(
        self,
        callback: Callable[[ChannelMessage], ChannelMessage],
        finish_callback: Callable,
        max_duration_in_sec: int = 0,
    ) -> None:
        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            self.handle(callback=callback, max_duration_in_sec=max_duration_in_sec)
        )

        loop.close()
        finish_callback()

    async def handle(
        self,
        callback: Callable[[ChannelMessage], ChannelMessage],
        max_duration_in_sec: int = 0,
    ):
        # establish the connection
        metadata: tuple = (
            *self.client.metadata,
            ("channel-id", self.id),
        )
        call = self.client.channel_client.ConnectChannelCustomer(metadata=metadata)

        await call.write(ChannelMessage())

        timeout_start = time.time()

        while time.time() < timeout_start + max_duration_in_sec:
            print("Waiting for message")
            incoming = await call.read()
            print(incoming)
            await call.write(callback(incoming))

        await call.done_writing()

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

        print("we finished!")

    def _listen_stream2(
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
            print("once")
            incoming_messages.put(msg)

        print("we finished!")

    @staticmethod
    def _handle_messages(
        incoming_msg_queue: queue.Queue,
        callback: Callable[[ChannelMessage], ChannelMessage],
    ) -> Iterator[ChannelMessage]:
        yield ChannelMessage()
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
