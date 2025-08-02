import socket
import json
import struct
from typing import Optional, Literal

from .stream_message import StreamMessage


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

    def send(self, command: str, payload: str) -> Optional[dict]:
        if not self.sock:
            self.status = "disconnected"
            raise ConnectionError("Socket is not connected.")

        message_bytes = StreamMessage(command, payload).to_bytes()

        try:
            self.sock.sendall(message_bytes)

            data =self.receive()

            return json.loads(data)
        except socket.timeout:
            self.close()
            raise TimeoutError(f"Operation timed out after {self.timeout} seconds")

    def _recv_exact(self, count: int) -> bytes:
        buf = b""
        while len(buf) < count:
            chunk = self.sock.recv(count - len(buf))
            if not chunk:
                raise ConnectionError("Connection closed")
            buf += chunk
        return buf

    def receive(self)-> str :
        len_prefix = self._recv_exact(4)
        msg_len = struct.unpack("<I", len_prefix)[0]
        payload = self._recv_exact(msg_len)
        return payload.decode("utf-8")

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            finally:
                self.sock.close()
        self.status = "disconnected"
