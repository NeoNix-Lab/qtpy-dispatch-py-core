from typing import Any, Callable, Dict, Optional, Type, TypeVar

from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)

class MessageEnvelope:
    """
    Wraps a DynamicMessage, delega serializzazione/deserializzazione,
    e invoca un callback alla ricezione.
    """

    def __init__(
            self,
            message: T,
            on_received: Optional[Callable[[T], None]] = None
    ) -> None:
        self.message = message
        self.on_received = on_received
        self._cls_type = type(message)
        self.dispatchable : Optional[T,None] = None

    @property
    def name(self) -> str:
        # Command = title
        return self.message.title if hasattr(self.message, "title") else self.message.__class__.__name__

    def set_sender(self, sender: T) -> None:
        self.dispatchable = sender

    def send(self):
        try:
            return self.dispatchable.model_dump_json(exclude_none=True)
        except Exception as e:
            print(e)
            return None


    def to_json(self) -> str:
        """
        Serializza il solo DynamicMessage in JSON:
        -> {"title": ..., "data": {...}}
        """
        return self.message.model_dump_json(exclude_none=True)

    def update_from_json(
            self,
            json_str: str,
    ) -> T:
        """
        Deserializza in msg, opzionalmente verifica il titolo,
        e sovrascrive self.message con la nuova istanza.
        """
        # 1) Deserializza correttamente
        msg: T = self._cls_type.model_validate_json(json_str)  # da dataclasses-json :contentReference[oaicite:1]{index=1}

        self.message = msg

        return msg

    def invoke(self, message : str) -> None:
        """
        Quando arriva il messaggio, invochi il callback passando
        l’oggetto DynamicMessage rigenerato.
        """
        self.update_from_json(message)
        if self.on_received:
            self.on_received(self.message)
