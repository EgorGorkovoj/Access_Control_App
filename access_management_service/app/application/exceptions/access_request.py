from .base import AppException


class RequestAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, request_id: str):
        super().__init__(f'Заявка с request_id:{request_id} уже существует!')


class RequestNotFoundError(AppException):
    status_code = 404

    def __init__(self, request_id: str):
        super().__init__(f'Заявки с request_id "{request_id}" не существует!')
