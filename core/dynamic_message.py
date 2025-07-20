from dataclasses import dataclass
from typing import Dict, Any
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DynamicMessage:
    title: str
    data: Dict[str, Any]
