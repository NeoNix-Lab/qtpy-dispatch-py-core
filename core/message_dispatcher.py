"""Dispatcher for :class:`~core.stream_message.StreamMessage` objects."""

from typing import Dict

from .message_envelope import MessageEnvelope
from stream_message import StreamMessage


class MessageDispatcher:
    """Route incoming messages to their registered envelopes."""

    def __init__(self) -> None:
        self._envelopes: Dict[str, MessageEnvelope] = {}

    def register(self, envelope: MessageEnvelope) -> None:
        """Register a new envelope for dispatch."""

        if envelope.name in self._envelopes:
            raise ValueError(f"Envelope for '{envelope.name}' already registered")
        self._envelopes[envelope.name] = envelope

    def dispatch(self, message: StreamMessage) -> None:
        """Dispatch ``message`` to the matching envelope, if registered."""

        if message.Command in self._envelopes:
            registered = self._envelopes[message.Command]
            registered.invoke(message.Payload)
        else:
            print(f"{message.Command} not registered")

