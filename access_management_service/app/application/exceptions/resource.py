from .base import AppException


class ResourceAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, resource_name: str, resource_type: str):
        super().__init__(
            f'Resource with name="{resource_name}" and type="{resource_type}" already exists.'
        )


class ResourceNotExistsError(AppException):
    status_code = 404

    def __init__(self, resource_id: int):
        super().__init__(f'Resource with id={resource_id} not found.')
