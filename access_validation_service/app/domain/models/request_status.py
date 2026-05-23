from enum import StrEnum


class RequestStatus(StrEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in progress'
    APPROVED = 'approved'
    REJECTED = 'rejected'
