from dataclasses import dataclass, field
from typing import Any


@dataclass
class Resource:
    id: int
    name: str
    type: str
    attributes: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True


@dataclass
class ResourceCreate:
    """Модель для создания ресурса (без id)"""

    name: str
    type: str
    attributes: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
