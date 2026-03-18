from dataclasses import dataclass


@dataclass
class Access:
    name: str
    description: str
    resource_id: int
    id: int | None = None
