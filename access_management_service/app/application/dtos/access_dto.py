from dataclasses import dataclass


@dataclass(slots=True)
class AccessDTO:
    id: int | None
    name: str
    description: str
    resource_id: int
