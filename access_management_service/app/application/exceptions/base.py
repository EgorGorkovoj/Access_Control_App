class AppException(Exception):
    status_code = 400
    detail = 'Application error'

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
