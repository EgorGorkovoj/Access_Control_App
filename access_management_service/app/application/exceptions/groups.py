from .base import AppException


class GroupAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_name: str):
        super().__init__(f'Group "{group_name}" already exists.')


class GroupNotExistsError(AppException):
    status_code = 404

    def __init__(self, group_id: int):
        super().__init__(f'Group with id={group_id} not found.')
