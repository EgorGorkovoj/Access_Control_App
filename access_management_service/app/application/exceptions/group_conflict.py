from .base import AppException


class GroupConflictWithItselfError(AppException):
    status_code = 400

    def __init__(self, group_id: int):
        super().__init__(f'Group {group_id} cannot conflict with itself.')


class GroupConflictAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_id: int, conflicting_group_id: int):
        super().__init__(
            f'Conflict between groups {group_id} and {conflicting_group_id} already exists.'
        )


class GroupConflictNotFoundError(AppException):
    status_code = 404

    def __init__(self, group_id: int, conflicting_group_id: int):
        super().__init__(
            f'Conflict between groups {group_id} and {conflicting_group_id} not found.'
        )
