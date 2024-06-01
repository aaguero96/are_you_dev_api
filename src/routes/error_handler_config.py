from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from errors import HttpError


class ErrorHandlerConfig:
    def __init__(self, app: FastAPI) -> None:
        self._app = app
        self.setup_error_handlers()

    def setup_error_handlers(self):
        @self._app.exception_handler(RequestValidationError)
        async def validation_error_handler(request: Request, exc: RequestValidationError):
            errors = exc.errors()
            field = errors[0].get("loc")[-1]
            message = errors[0].get("msg")
            if message.find("required"):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": f"field {field} is required"}
                )
            
        @self._app.exception_handler(HttpError)
        async def http_error_handler(request: Request, exc: HttpError):
            return JSONResponse(
                status_code=exc.code,
                content={"message": exc.message}
            )
        
        @self._app.exception_handler(ValueError)
        async def http_error_handler(request: Request, exc: ValueError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "internal server error"}
            )
    