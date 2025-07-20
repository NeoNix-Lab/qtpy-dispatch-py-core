import socket
import json
import struct
from typing import Optional, Literal

from stream_message import StreamMessage


class SocketClientService:
    """A TCP client that sends and receives length-prefixed JSON messages."""

    def __init__(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.status: Literal["disconnected", "connected"] = "disconnected"
        self.sock: Optional[socket.socket] = None

    def connect(self) -> None:
        try:
            if self.timeout is not None:
                self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
                self.sock.settimeout(self.timeout)
            else:
                self.sock = socket.create_connection((self.host, self.port))
            self.status = "connected"
        except socket.timeout:
            if self.sock:
                self.sock.close()
            self.status = "disconnected"
            raise TimeoutError(f"Connect timed out after {self.timeout} seconds")

    async def send(self, command: str, payload: str) -> Optional[dict]:
        if not self.sock:
            self.status = "disconnected"
            raise ConnectionError("Socket is not connected.")

        message_bytes = StreamMessage(command, payload).to_bytes()

        try:
            self.sock.sendall(message_bytes)

            len_prefix = b""
            while len(len_prefix) < 4:
                chunk = self.sock.recv(4 - len(len_prefix))
                if not chunk:
                    return None
                len_prefix += chunk
            msg_len = struct.unpack("<I", len_prefix)[0]

            data = b""
            while len(data) < msg_len:
                chunk = self.sock.recv(msg_len - len(data))
                if not chunk:
                    break
                data += chunk

            return json.loads(data.decode("utf-8"))
        except socket.timeout:
            self.close()
            raise TimeoutError(f"Operation timed out after {self.timeout} seconds")

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            finally:
                self.sock.close()
        self.status = "disconnected"
