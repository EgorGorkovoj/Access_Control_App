from .base import AppException


class GroupConflictWithItselfError(AppException):
    status_code = 400

    def __init__(self, group_id: int):
        super().__init__(f'Группа {group_id} не может конфликтовать сама с собой!')


class GroupConflictAlreadyExistsError(AppException):
    status_code = 409

    def __init__(self, group_id: int, conflicting_group_id: int):
        super().__init__(
            f'Конфликт между группами {group_id} и {conflicting_group_id} уже существует!'
        )


class GroupConflictNotFoundError(AppException):
    status_code = 404

    def __init__(self, group_id: int, conflicting_group_id: int):
        super().__init__(
            f'Конфликтующих групп с ID {group_id} и {conflicting_group_id} не обнаружено!'
        )
