from __future__ import annotations

import asyncio
import logging
from typing import List, Callable, Optional, Awaitable

from google.protobuf import empty_pb2

from tq42.exception_handling import handle_generic_sdk_errors
from com.terraquantum.channel.v1alpha1.create_channel_pb2 import CreateChannelResponse

# important for re-export
from com.terraquantum.channel.v1alpha1.channel_message_pb2 import (
    ChannelMessage,
    Ask,
    Parameter,  # pylint:disable=unused-import # noqa: F401
    Tell,
    DataAcknowledge,
)

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


from tq42.utils.timers import AsyncTimedIterable


class Channel:
    """
    Class to create and connect to a channel
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
    async def create(client: TQ42Client) -> Channel:
        empty = empty_pb2.Empty()
        res: CreateChannelResponse = await client.channel_client.CreateChannel(
            request=empty, metadata=client.metadata
        )
        return Channel(client=client, id=res.channel_id)

    async def connect(
        self,
        callback: Callable[[Ask], Awaitable[Tell]],
        finish_callback: Callable,
        max_duration_in_sec: Optional[int] = None,
        message_timeout_in_sec: Optional[int] = None,
    ) -> None:
        """
        Connects to the stream and handles every message with the provided callback to create an answer.
        ASK gets into the callback and then we expect a TELL answer

        :param callback: Async callback that handles an ASK message and returns a TELL message
        :param finish_callback: Callback that is called when channel is completed
        :param int max_duration_in_sec: Timeout for whole connection in seconds. `None` -> no timeout for overall flow
        :param int message_timeout_in_sec: Timeout between messages in seconds. `None` -> no timeout between messages
        """

        async def _acknowledge_message(msg: ChannelMessage) -> None:
            ack_msg = ChannelMessage(
                acknowledge_data=DataAcknowledge(id=msg.sequential_message_id)
            )
            await call.write(ack_msg)
            logging.debug(f"User Sent ack {msg.sequential_message_id=}")

        async def _handle():
            try:
                timed_stream = AsyncTimedIterable(call, timeout=message_timeout_in_sec)
                incoming: ChannelMessage
                async for incoming in timed_stream:
                    logging.debug(f"User received {incoming=}")
                    data_field_name = incoming.WhichOneof("data")
                    if data_field_name == "completion_data":
                        await _acknowledge_message(msg=incoming)
                        logging.debug(
                            "Message indicated channel completion. Closing channel connection"
                        )
                        break
                    elif data_field_name == "ask_data":
                        tell = await callback(incoming.ask_data)
                        await _acknowledge_message(msg=incoming)
                        tell_msg = ChannelMessage(
                            sequential_message_id=(incoming.sequential_message_id + 1),
                            tell_data=tell,
                        )
                        await call.write(tell_msg)

            except asyncio.TimeoutError:
                logging.debug("Stream finished because of the provided timeouts")
                raise TimeoutError(
                    f"Channel was closed due to exceeding {message_timeout_in_sec}s timeout between messages"
                ) from None

        metadata: tuple = (
            *self.client.metadata,
            ("channel-id", self.id),
        )
        call = self.client.channel_client.ConnectChannelCustomer(metadata=metadata)

        await call.write(ChannelMessage())
        await asyncio.wait_for(_handle(), timeout=max_duration_in_sec)
        await call.done_writing()

        finish_callback()


@handle_generic_sdk_errors
def list_all(client: TQ42Client) -> List[Channel]:
    """
    List all channels for a given user.

    For details, see (TODO: update link once a new documentation URL is created)
    """
    raise NotImplementedError("This is a functionality still to come")
