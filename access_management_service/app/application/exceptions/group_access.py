from .base import AppException


class GroupAccessAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_id: int, access_id: int):
        super().__init__(
            f'Group access with group_id={group_id} and access_id={access_id} already exists.'
        )


class GroupAccessNotFoundError(AppException):
    status_code = 404

    def __init__(self, group_id: int, access_id: int):
        super().__init__(
            f'Group access with group_id={group_id} and access_id={access_id} not found.'
        )
