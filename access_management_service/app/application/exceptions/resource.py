from .base import AppException


class ResourceAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, resource_name: str, resource_type: str):
        super().__init__(
            f'Ресурс с именем {resource_name} и типом {resource_type} уже существует!'
        )


class ResourceNotExistsError(AppException):
    status_code = 404

    def __init__(self, resource_id: int):
        super().__init__(f'Ресурса с id:{resource_id} не существует!')
