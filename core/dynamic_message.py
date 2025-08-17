"""Basic container for dynamic JSON messages."""

from dataclasses import dataclass
from typing import Any, Dict

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DynamicMessage:
    """Represents a generic JSON message.

    Attributes
    ----------
    title:
        Short string identifying the message type.
    data:
        Arbitrary payload encoded as a dictionary.
    """

    title: str
    data: Dict[str, Any]

