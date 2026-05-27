from app.application.exceptions.base import AppException


class UserGroupAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, user_id: int, group_id: int):
        super().__init__(f'User with id={user_id} already belongs to group with id={group_id}.')


class UserGroupNotFoundError(AppException):
    status_code = 404

    def __init__(self, user_id: int, group_id: int):
        super().__init__(f'User with id={user_id} does not belong to group with id={group_id}.')
