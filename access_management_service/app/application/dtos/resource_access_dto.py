from dataclasses import dataclass
from typing import Any


@dataclass
class AccessCredentialsDTO:
    id: int
    name: str
    credentials: dict[str, Any]
    description: str | None = None


@dataclass
class ResourceAccessesDTO:
    resource_id: int
    resource_name: str
    resource_type: str
    accesses: list[AccessCredentialsDTO]
