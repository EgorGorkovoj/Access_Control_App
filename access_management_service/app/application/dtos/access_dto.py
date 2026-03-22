from dataclasses import dataclass


@dataclass
class AccessDTO:
    id: int | None
    name: str
    description: str | None
    resource_id: int


@dataclass
class CreateAccessDTO:
    name: str
    description: str | None
    resource_id: int
