from .base import AppException


class GroupAccessAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_id: int, access_id: int):
        super().__init__(
            f'Группа доступов с group_id:{group_id}" и access_id:{access_id} уже существует!'
        )


class GroupAccessNotFoundError(AppException):
    status_code = 404

    def __init__(self, group_id: int, access_id: int):
        super().__init__(
            f'Группы доступов с group_id:{group_id} и access_id:{access_id} не существует!'
        )
