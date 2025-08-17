"""Facade for managing socket communication and message dispatching."""

from __future__ import annotations

import json
import threading
from threading import RLock
from typing import Literal, Optional

from core.dispatcher import Dispatcher
from core.message_envelope import MessageEnvelope
from core.socket_manager import SocketManager


class _Hub:
    """Manage a socket client and dispatch received messages."""

    def __init__(self) -> None:
        self.client: Optional[SocketManager] = None
        self.dispatcher: Optional[Dispatcher] = None
        self.status: Literal["Connected", "Disconnected", "Listening"] = "Disconnected"
        self._t: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._lock = RLock()  # thread-safe

    def connect(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        """Connect to a remote hub and start listening."""

        with self._lock:
            self.client = SocketManager.connect(host, port, timeout)
            self.dispatcher = Dispatcher()
            self.status = "Connected"
            self._listen()

    def _listen(self) -> None:
        """Start the background receive loop."""

        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self._stop.clear()
        if self._t and self._t.is_alive():
            return
        self._t = threading.Thread(target=self._rx_loop, name="rx-loop", daemon=False)
        self._t.start()
        with self._lock:
            self.status = "Listening"

    def _rx_loop(self) -> None:
        """Background thread that receives and dispatches messages."""

        while not self._stop.is_set():
            raw = self.client.receive()
            obj = json.loads(raw)
            title = obj.get("Title") or obj.get("title") or obj.get("MessageType")
            try:
                self.dispatcher.dispatch(title, raw)
            except Exception as e:
                with self._lock:
                    self.status = "Connected"
                print(f"dispatch error ___ {e}")

    def register(self, envelop: MessageEnvelope) -> None:
        """Register a message envelope with the dispatcher."""

        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.register(envelop)

    def clear_dispatcher(self) -> None:
        """Remove all envelopes from the dispatcher."""

        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.clear()

    def unregister(self, envelop: MessageEnvelope) -> None:
        """Unregister the given envelope from the dispatcher."""

        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.unregister(envelop)

    def send_dispatcher(self, message: MessageEnvelope) -> None:
        """Serialize and send ``message`` via the socket client."""

        if not self.client:
            raise RuntimeError("Not connected")
        self.client.send(message.send())

    def send_name(self, dispatcher_name: str) -> None:
        """Send a message by its dispatcher name."""

        if not self.client:
            raise RuntimeError("Not connected")
        message = self.dispatcher.send(dispatcher_name)
        self.client.send(message)

    def send_object(self, dispatcher_name: str, obj) -> None:
        """Attach ``obj`` as sender and dispatch the message."""

        if not self.client:
            raise RuntimeError("Not connected")
        self.dispatcher.set_sender(dispatcher_name, obj)
        message = self.dispatcher.send(dispatcher_name)
        self.client.send(message)

    def disconnect(self) -> None:
        """Stop the receive loop and close the client connection."""

        with self._lock:
            self._stop.set()
            if self.client:
                self.client.close()
        if self._t:
            self._t.join(timeout=5)
            self._t = None
        with self._lock:
            self.client = None
            self.dispatcher = None
            self.status = "Disconnected"


_hub = _Hub()

# Public facade functions
connect = _hub.connect
send_obj = _hub.send_object
send_name = _hub.send_name
send_dispatcher = _hub.send_dispatcher
disconnect = _hub.disconnect
register = _hub.register
unregister = _hub.unregister
clear_dispatcher = _hub.clear_dispatcher


def get_status() -> str:
    """Return the current hub status."""

    return _hub.status


def get_client() -> SocketManager:
    """Return the underlying :class:`SocketManager`."""

    return _hub.client


def get_dispatcher() -> Dispatcher:
    """Return the current :class:`Dispatcher`."""

    return _hub.dispatcher


def get_sandables():
    """Return all sendable objects currently registered."""

    return _hub.dispatcher.sendablees


def get_sandable(name: str):
    """Return the sendable object identified by ``name``."""

    return _hub.dispatcher.sendable(name)


def get_messages():
    """Return all registered message objects."""

    return _hub.dispatcher.messages


def get_message(name: str):
    """Return the message object identified by ``name``."""

    return _hub.dispatcher.message(name)


def set_sender(envelope: str, sender):
    """Attach ``sender`` to the envelope identified by ``envelope``."""

    return _hub.dispatcher.set_sender(envelope, sender)


def create_envelop(message, on_recive) -> MessageEnvelope | None:
    """Create a :class:`MessageEnvelope` and return ``None`` on error."""

    try:
        return MessageEnvelope(message, on_recive)
    except Exception as e:
        print(e)
        return None
