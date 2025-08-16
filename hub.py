from __future__ import annotations
import json
from typing import Optional, Literal, Callable
from threading import RLock
import threading
from core.socket_manager import SocketManager
from core.dispatcher import Dispatcher
from core.message_envelope import MessageEnvelope

class _Hub:
    def __init__(self) -> None:
        self.client: Optional[SocketManager] = None
        self.dispatcher: Optional[Dispatcher] = None
        self.status: Literal["Connected","Disconnected","Listening"] = "Disconnected"
        self._t: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._lock = RLock()  # thread-safe

    def connect(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        with self._lock:
            self.client = SocketManager.connect(host, port, timeout)
            self.dispatcher = Dispatcher()
            self.status = "Connected"
            self._listen()

    def _listen(self) -> None:
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
        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.register(envelop)

    def clear_dispatcher(self) -> None:
        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.clear()

    def unregister(self, envelop: MessageEnvelope) -> None:
        if not self.client or not self.dispatcher:
            raise RuntimeError("Not connected")
        self.dispatcher.unregister(envelop)

    def send_dispatcher(self, message: MessageEnvelope) -> None:
        if not self.client:
            raise RuntimeError("Not connected")
        self.client.send(message.send())

    def send_name(self, dispatcher_name: str) -> None:
        if not self.client:
            raise RuntimeError("Not connected")
        message = self.dispatcher.send(dispatcher_name)
        self.client.send(message)

    def send_object(self, dispatcher_name: str, object) -> None:
        if not self.client:
            raise RuntimeError("Not connected")
        self.dispatcher.set_sender(dispatcher_name, object)
        message = self.dispatcher.send(dispatcher_name)
        self.client.send(message)

    def disconnect(self) -> None:
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

# --- API pubblica (facade) ---
connect = _hub.connect
send_obj = _hub.send_object
send_name = _hub.send_name
send_dispatcher = _hub.send_dispatcher
disconnect = _hub.disconnect
register      = _hub.register
unregister    = _hub.unregister
clear_dispatcher = _hub.clear_dispatcher

def get_status() -> str:
    return _hub.status
def get_client() -> SocketManager:
    return _hub.client
def get_dispatcher() -> Dispatcher:
    return _hub.dispatcher
def get_sandables():
    return _hub.dispatcher.sendablees
def get_sandable(name: str):
    return _hub.dispatcher.sendable(name)
def get_messages():
    return _hub.dispatcher.messages
def get_message(name: str):
    return _hub.dispatcher.message(name)
def set_sender(envelope : str, sender):
    return  _hub.dispatcher.set_sender(envelope, sender)
def create_envelop(message, on_recive) -> MessageEnvelope or None:
    try:
        return MessageEnvelope(message, on_recive)
    except Exception as e:
        print(e)
        return None