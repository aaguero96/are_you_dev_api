from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class SwaggerConfig:
    def __init__(self, app: FastAPI) -> None:
        self._app = app

    def apply(self):
        schema = get_openapi(
            title="Are you dev API",
            version="1.0.0",
            routes=self._app.routes,
        )
        self._app.openapi_schema = schema