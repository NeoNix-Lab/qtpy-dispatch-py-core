import json
import struct


class StreamMessage:
    """Represents a length-prefixed JSON message with a command and payload."""

    def __init__(self, command: str, payload: str) -> None:
        self.Command = command
        self.Payload = payload

    def to_bytes(self) -> bytes:
        raw = json.dumps(self.__dict__).encode("utf-8")
        length_prefix = struct.pack("<I", len(raw))
        return length_prefix + raw

    @classmethod
    def from_bytes(cls, data: bytes) -> "StreamMessage":
        """
        Legge un blocco completo [4 byte length][raw JSON], ritorna l’oggetto.
        """
        if len(data) < 4:
            raise ValueError("Dati troppo corti per contenere il prefisso di lunghezza")
        length, = struct.unpack("<I", data[:4])
        json_raw = data[4:4+length].decode("utf-8")
        obj = json.loads(json_raw)
        return cls(command=obj["Command"], payload=obj["Payload"])
