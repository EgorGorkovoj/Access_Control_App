from dataclasses import dataclass


@dataclass
class RightGroupDTO:
    id: int | None
    name: str
    description: str | None = None


@dataclass
class CreateRightGroupDTO:
    name: str
    description: str | None = None


@dataclass
class UpdateRightGroupDTO:
    id: int
    name: str | None = None
    description: str | None = None
