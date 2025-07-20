from typing import Any, Callable, Dict, Optional, Type, TypeVar

from .dynamic_message import DynamicMessage

T = TypeVar('T', bound=DynamicMessage)

class MessageEnvelope:
    """
    Wraps a DynamicMessage, delega serializzazione/deserializzazione,
    e invoca un callback alla ricezione.
    """

    def __init__(
            self,
            message: DynamicMessage,
            on_received: Optional[Callable[[DynamicMessage], None]] = None
    ) -> None:
        self.message = message
        self.on_received = on_received

    @property
    def name(self) -> str:
        # Command = title
        return self.message.title

    @property
    def data(self) -> Dict[str, Any]:
        # Payload raw
        return self.message.data

    def to_json(self) -> str:
        """
        Serializza il solo DynamicMessage in JSON:
        -> {"title": ..., "data": {...}}
        """
        return self.message.to_json()

    def update_from_json(
            self,
            json_str: str,
            msg_cls: Type[T]
    ) -> T:
        """
        Deserializza in msg, opzionalmente verifica il titolo,
        e sovrascrive self.message con la nuova istanza.
        """
        # 1) Deserializza correttamente
        msg: T = msg_cls.from_json(json_str)  # da dataclasses-json :contentReference[oaicite:1]{index=1}

        # 2) (Opzionale) sanity check – confronta con il titolo corrente
        if msg.title != self.message.title:
            raise ValueError(f"Title mismatch: got {msg.title!r}, expected {self.message.title!r}")

        # 3) Sovrascrivi la proprietà
        self.message = msg

        return msg

    def invoke(self) -> None:
        """
        Quando arriva il messaggio, invochi il callback passando
        l’oggetto DynamicMessage rigenerato.
        """
        if self.on_received:
            self.on_received(self.message)
