"""Helpers for length-prefixed JSON socket communication."""

import socket
import struct
from typing import Optional


class SocketManager:
    """Utility wrapper around a ``socket`` instance."""

    def __init__(self, sock: socket.socket) -> None:
        """Store the underlying socket."""

        self.sock = sock

    @classmethod
    def connect(
        cls, host: str, port: int, timeout: Optional[float] = None
    ) -> "SocketManager":
        """Create a socket connection and return a manager for it."""

        sock = socket.create_connection((host, port), timeout)
        if timeout is not None:
            sock.settimeout(timeout)
        return cls(sock)

    def _recv_exact(self, count: int) -> bytes:
        """Read exactly ``count`` bytes from the socket."""

        buf = b""
        while len(buf) < count:
            chunk = self.sock.recv(count - len(buf))
            if not chunk:
                raise ConnectionError("Connection closed")
            buf += chunk
        return buf

    def send(self, json_str: str) -> None:
        """Send a JSON string with a little-endian length prefix."""

        data = json_str.encode("utf-8")
        prefix = struct.pack("<I", len(data))
        self.sock.sendall(prefix + data)

    def receive(self) -> str:
        """Receive a length-prefixed JSON string."""

        len_prefix = self._recv_exact(4)
        msg_len = struct.unpack("<I", len_prefix)[0]
        payload = self._recv_exact(msg_len)
        return payload.decode("utf-8")

    def close(self) -> None:
        """Close the managed socket safely."""

        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        finally:
            self.sock.close()
