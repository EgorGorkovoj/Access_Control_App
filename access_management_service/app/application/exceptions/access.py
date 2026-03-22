from .base import AppException


class AccessAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, name: str, resource_id: int):
        super().__init__(f'Доступ с именем {name} и ресурсом id:{resource_id} уже существует!')


class AccessNotFoundError(AppException):
    status_code = 404

    def __init__(self, access_id: int):
        super().__init__(f'Доступа с id "{access_id}" не существует!')
