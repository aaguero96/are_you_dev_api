from fastapi import HTTPException


class HttpError(HTTPException):
    def __init__(self, message: str, code: int, stack: ValueError = None) -> None:
        self.message = message
        self.code = code
        self.stack = stack
        super().__init__(status_code=code, detail=message)