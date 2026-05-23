from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResourceDTO:
    id: int
    name: str
    type: str
    is_active: bool
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class CreateResourceDTO:
    name: str
    type: str
    attributes: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True


@dataclass
class UpdateResourceDTO:
    id: int
    name: str | None = None
    type: str | None = None
    attributes: dict[str, Any] | None = None
    is_active: bool | None = None
