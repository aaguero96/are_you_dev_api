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
        @self.router.post(
            "/",
            response_model=CreateUserResponseDTO | ErrorResponseDTO,
            tags=["user"],
            summary="Create user",
            responses={
                status.HTTP_201_CREATED: {"model": CreateUserResponseDTO, "description": "success"},
                status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseDTO, "description": "bad request"},
                status.HTTP_409_CONFLICT: {"model": ErrorResponseDTO, "description": "conflict"},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponseDTO, "description": "internal server error"},
            },
        )
        def create(request: CreateUserRequestDTO, response: Response):
            return self._user_controller.create(request, response)
            
        @self.router.post(
            "/login",
            response_model=LoginResponseDTO | ErrorResponseDTO,
            tags=["user"],
            responses={
                status.HTTP_200_OK: {"model": CreateUserResponseDTO, "description": "success"},
                status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseDTO, "description": "bad request"},
                status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseDTO, "description": "unauthorized"},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponseDTO, "description": "internal server error"},
            },
        )
        def login(request: LoginRequestDTO, response: Response):
            return self._user_controller.login(request, response)

