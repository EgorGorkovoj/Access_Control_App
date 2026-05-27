from .base import AppException


class RequestAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, request_id: str):
        super().__init__(f'Request "{request_id}" already exists.')


class RequestNotFoundError(AppException):
    status_code = 404

    def __init__(self, request_id: str):
        super().__init__(f'Request "{request_id}" not found.')
