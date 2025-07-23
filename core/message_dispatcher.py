from typing import Dict
from .message_envelope import MessageEnvelope
from stream_message import StreamMessage


class MessageDispatcher:
    """Routes incoming JSON messages to the registered envelopes."""

    def __init__(self) -> None:
        self._envelopes: Dict[str, MessageEnvelope] = {}

    def register(self, envelope: MessageEnvelope) -> None:
        if envelope.name in self._envelopes:
            raise ValueError(f"Envelope for '{envelope.name}' already registered")
        self._envelopes[envelope.name] = envelope

    def dispatch(self, json_str: StreamMessage) -> None:
       if json_str.Command in self._envelopes:
            registered = self._envelopes[json_str.Command]
            registered.update_from_json(json_str.Payload)
            registered.invoke()