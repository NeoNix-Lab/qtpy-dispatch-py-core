from .message_envelope import MessageEnvelope
from typing import Dict

class Dispatcher:
    def __init__(self):
        self._enveloped : Dict[str, MessageEnvelope] = {}

    def register(self, envelop : MessageEnvelope) -> None:
        if envelop.name not in  self._enveloped:
            self._enveloped[envelop.name] = envelop
        else:
            print(f"{envelop.name} already registered")

    def set_sender(self, envelope : str, sender):
        if envelope in self._enveloped:
            self._enveloped[envelope].set_sender(sender)
        else:
            print(f"{envelope} not registered")

    def send(self, envelope : str):
        if envelope in self._enveloped:
            return  self._enveloped[envelope].send()
        else:
            print(f"{envelope} not registered")
            return None

    def clear(self):
        self._enveloped = dict()

    def unregister(self, envelope : str) -> None:
        if envelope in self._enveloped:
            self._enveloped.pop(envelope)
        else:
            print(f"{envelope} not registered")

    def dispatch(self, envelope_name:str, message:str):
        if envelope_name in self._enveloped:
            self._enveloped[envelope_name].invoke(message)
        else:
            print(f"{envelope_name} not registered")

    @property
    def messages(self) -> list:
        # Command = title
        return [obj.message for obj in self._enveloped.values()]

    @property
    def sendablees(self) -> list:
        return [obj.dispatchable for obj in self._enveloped.values()]

    def message(self, name : str) -> object:
        if name in self._enveloped:
            return self._enveloped[name].message
        else:
            return None

    def sendable(self, name : str) -> object:
        if name in self._enveloped:
            return self._enveloped[name].dispatchable
        else:
            return None