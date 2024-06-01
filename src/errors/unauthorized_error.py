from .http_error import HttpError
from fastapi import status


class UnauthorizedError(HttpError):
    def __init__(self, message: str, stack: ValueError = None) -> None:
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, stack)