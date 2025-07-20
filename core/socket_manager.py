import socket
import struct
from typing import Optional


class SocketManager:
    """Utility class for length-prefixed JSON socket communication."""

    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock

    @classmethod
    def connect(cls, host: str, port: int, timeout: Optional[float] = None) -> "SocketManager":
        sock = socket.create_connection((host, port), timeout)
        if timeout is not None:
            sock.settimeout(timeout)
        return cls(sock)

    def _recv_exact(self, count: int) -> bytes:
        buf = b""
        while len(buf) < count:
            chunk = self.sock.recv(count - len(buf))
            if not chunk:
                raise ConnectionError("Connection closed")
            buf += chunk
        return buf

    def send(self, json_str: str) -> None:
        data = json_str.encode("utf-8")
        prefix = struct.pack("<I", len(data))
        self.sock.sendall(prefix + data)

    def receive(self) -> str:
        len_prefix = self._recv_exact(4)
        msg_len = struct.unpack("<I", len_prefix)[0]
        payload = self._recv_exact(msg_len)
        return payload.decode("utf-8")

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        finally:
            self.sock.close()
