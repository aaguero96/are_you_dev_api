from fastapi import APIRouter, Response, status
from dtos import (
    CreateUserRequestDTO,
    CreateUserResponseDTO,
    LoginRequestDTO,
    LoginResponseDTO,
    ErrorResponseDTO,
)
from controllers import IUserController
from errors import HttpError


class UserRoute:
    def __init__(self, user_controller: IUserController) -> None:
        self.router = APIRouter(prefix="/user")
        self._user_controller = user_controller
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/", response_model=CreateUserResponseDTO | ErrorResponseDTO, tags=["user"], summary="Create user")
        def create(request: CreateUserRequestDTO, response: Response):
            try:
                res = self._user_controller.create(request)
                response.status_code = status.HTTP_201_CREATED
                return res
            except HttpError as err:
                response.status_code = err.code
                return {"message": err.message}
            except ValueError as err:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"message": "internal server error"}
            
        @self.router.post("/login", response_model=LoginResponseDTO | ErrorResponseDTO, tags=["user"])
        def login(request: LoginRequestDTO, response: Response):
            try:
                res = self._user_controller.login(request)
                response.status_code = status.HTTP_201_CREATED
                return res
            except HttpError as err:
                response.status_code = err.code
                return {"message": err.message}
            except ValueError as err:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"message": "internal server error"}
