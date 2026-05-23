class ValidationError(Exception):
    """Базовая ошибка валидации."""

    pass


class GroupConflictError(ValidationError):
    def __init__(
        self,
        user_id: int,
        target_group_id: int,
    ):
        self.user_id = user_id
        self.target_group_id = target_group_id

        super().__init__(
            f'User {user_id} has conflicting group for target group {target_group_id}'
        )


class AccessConflictError(ValidationError):
    def __init__(
        self,
        user_id: int,
        access_id: int,
    ):
        self.user_id = user_id
        self.access_id = access_id

        super().__init__(
            f'User {user_id} cannot receive access {access_id} because of conflicting groups'
        )
