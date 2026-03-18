from .base import AppException


class GroupAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_name: str):
        super().__init__(f'Группа "{group_name}" уже существует!')


class GroupNotExistsError(AppException):
    status_code = 404

    def __init__(self, group_id: int):
        super().__init__(f'Группы с id "{group_id}" не существует!')
