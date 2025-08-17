"""Simple in-memory dispatcher for :class:`MessageEnvelope` instances."""

from typing import Dict

from .message_envelope import MessageEnvelope


class Dispatcher:
    """Manage a collection of message envelopes and dispatch messages."""

    def __init__(self) -> None:
        self._enveloped: Dict[str, MessageEnvelope] = {}

    def register(self, envelope: MessageEnvelope) -> None:
        """Register a new envelope by its name."""

        if envelope.name not in self._enveloped:
            self._enveloped[envelope.name] = envelope
        else:
            print(f"{envelope.name} already registered")

    def set_sender(self, envelope: str, sender) -> None:
        """Attach a sender object to the specified envelope."""

        if envelope in self._enveloped:
            self._enveloped[envelope].set_sender(sender)
        else:
            print(f"{envelope} not registered")

    def send(self, envelope: str):
        """Serialize the sender associated with an envelope."""

        if envelope in self._enveloped:
            return self._enveloped[envelope].send()
        else:
            print(f"{envelope} not registered")
            return None

    def clear(self) -> None:
        """Remove all registered envelopes."""

        self._enveloped = dict()

    def unregister(self, envelope: str) -> None:
        """Remove an envelope from the dispatcher."""

        if envelope in self._enveloped:
            self._enveloped.pop(envelope)
        else:
            print(f"{envelope} not registered")

    def dispatch(self, envelope_name: str, message: str) -> None:
        """Invoke the envelope's callback with the provided message."""

        if envelope_name in self._enveloped:
            self._enveloped[envelope_name].invoke(message)
        else:
            print(f"{envelope_name} not registered")

    @property
    def messages(self) -> list:
        """Return the current messages for all envelopes."""

        # Command = title
        return [obj.message for obj in self._enveloped.values()]

    @property
    def sendablees(self) -> list:
        """Return sender objects for all envelopes."""

        return [obj.dispatchable for obj in self._enveloped.values()]

    def message(self, name: str):
        """Return the message associated with *name* if present."""

        if name in self._enveloped:
            return self._enveloped[name].message
        else:
            return None

    def sendable(self, name: str):
        """Return the sender associated with *name* if present."""

        if name in self._enveloped:
            return self._enveloped[name].dispatchable
        else:
            return None
