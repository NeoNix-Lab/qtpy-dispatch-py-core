"""Representation of length-prefixed JSON messages."""

import json
import struct


class StreamMessage:
    """Container for a command and payload transmitted over sockets."""

    def __init__(self, command: str, payload: str) -> None:
        """Store the command name and JSON payload."""

        self.Command = command
        self.Payload = payload

    def to_bytes(self) -> bytes:
        """Serialize the message to ``[length][JSON]`` bytes."""

        raw = json.dumps(self.__dict__).encode("utf-8")
        length_prefix = struct.pack("<I", len(raw))
        return length_prefix + raw

    @classmethod
    def from_bytes(cls, data: bytes) -> "StreamMessage":
        """Parse ``data`` into a :class:`StreamMessage` instance."""

        if len(data) < 4:
            raise ValueError("Data too short to contain length prefix")
        length, = struct.unpack("<I", data[:4])
        json_raw = data[4 : 4 + length].decode("utf-8")
        obj = json.loads(json_raw)
        return cls(command=obj["Command"], payload=obj["Payload"])

