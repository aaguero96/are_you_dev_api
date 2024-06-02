from .http_error import HttpError
from fastapi import status


class InternalServerError(HttpError):
    def __init__(self, stack: ValueError = None) -> None:
        super().__init__("internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR, stack)