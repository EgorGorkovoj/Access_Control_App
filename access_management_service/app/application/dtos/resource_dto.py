from dataclasses import dataclass
from typing import Any


@dataclass
class ResourceDTO:
    id: int | None
    name: str
    type: str
    attributes: dict[str, Any]


@dataclass
class CreateResourceDTO:
    name: str
    type: str
    attributes: dict[str, Any]


@dataclass
class UpdateResourceDTO:
    id: int
    name: str | None = None
    type: str | None = None
    attributes: dict[str, Any] | None = None
