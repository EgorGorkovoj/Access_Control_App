from dataclasses import dataclass
from typing import Any


@dataclass
class AccessDTO:
    id: int
    name: str
    resource_id: int
    credentials: dict[str, Any]
    description: str | None = None
    is_active: bool = True


@dataclass
class CreateAccessDTO:
    name: str
    resource_id: int
    credentials: dict[str, Any]
    description: str | None = None
    is_active: bool = True
