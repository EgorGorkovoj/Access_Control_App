from dataclasses import dataclass
from typing import Any


@dataclass
class Resource:
    name: str
    type: str
    attributes: dict[str, Any]
    id: int | None = None
