from app.application.exceptions.base import AppException


class UserAlreadyHasAccessError(AppException):
    status_code = 409

    def __init__(self, user_id: int, access_id: int):
        super().__init__(f'User with id={user_id} already has access with id={access_id}.')


class UserDoesNotHaveAccessError(AppException):
    status_code = 404

    def __init__(self, user_id: int, access_id: int):
        super().__init__(f'User with id={user_id} does not have access with id={access_id}.')
