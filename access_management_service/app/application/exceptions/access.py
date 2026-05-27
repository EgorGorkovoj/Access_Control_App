from .base import AppException


class AccessAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, name: str, resource_id: int):
        super().__init__(
            f'Access with name="{name}" and resource_id={resource_id} already exists.'
        )


class AccessNotFoundError(AppException):
    status_code = 404

    def __init__(self, access_id: int):
        super().__init__(f'Access with id={access_id} not found.')
