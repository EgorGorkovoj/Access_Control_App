from dataclasses import dataclass


@dataclass
class ResourceAccessesDTO:
    resource_id: int
    resource_name: str
    resource_type: str
    accesses: list['AccessCredentialsDTO']


@dataclass
class AccessCredentialsDTO:
    id: int
    name: str
    description: str | None
    credentials: dict
