from dataclasses import dataclass


@dataclass
class RightGroup:
    name: str
    description: str | None = None
    id: int | None = None
