"""Utilities for wrapping messages with metadata and callbacks."""

from typing import Any, Callable, Dict, Optional, Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class MessageEnvelope:
    """Wraps a message and optional callback for dispatching.

    Parameters
    ----------
    message:
        The message instance to manage.
    on_received:
        Optional function invoked when a message is received.
    """

    def __init__(
            self,
            message: T,
            on_received: Optional[Callable[[T], None]] = None
    ) -> None:
        self.message = message
        self.on_received = on_received
        self._cls_type = type(message)
        self.dispatchable: Optional[T, None] = None

    @property
    def name(self) -> str:
        """Return the logical name of the message."""

        # Command = title
        return (
            self.message.title
            if hasattr(self.message, "title")
            else self.message.__class__.__name__
        )

    def set_sender(self, sender: T) -> None:
        """Associate an object used to send this message."""

        self.dispatchable = sender

    def send(self) -> Optional[str]:
        """Serialize the dispatchable sender to JSON if available."""

        try:
            return self.dispatchable.model_dump_json(exclude_none=True)
        except Exception as e:
            print(e)
            return None


    def to_json(self) -> str:
        """Serialize only the encapsulated message to JSON."""

        return self.message.model_dump_json(exclude_none=True)

    def update_from_json(self, json_str: str) -> T:
        """Update ``self.message`` from a JSON string and return it."""

        msg: T = self._cls_type.model_validate_json(json_str)
        self.message = msg
        return msg

    def invoke(self, message: str) -> None:
        """Process an incoming message and trigger the callback if set."""

        self.update_from_json(message)
        if self.on_received:
            self.on_received(self.message)
