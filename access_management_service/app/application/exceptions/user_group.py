from app.application.exceptions.base import AppException


class UserGroupAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, user_id: int, group_id: int):
        super().__init__(f'Пользователь с id:{user_id} уже имеет группу c id:{group_id}!')


class UserGroupNotFoundError(AppException):
    status_code = 404

    def __init__(self, user_id: int, group_id: int):
        super().__init__(f'Пользователя с id:{user_id} и группой с id:{group_id} не существует!')
