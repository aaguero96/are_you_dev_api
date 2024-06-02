from abc import ABC, abstractmethod
from services import IUserService
from models import UserModel
from dtos import (
    CreateUserRequestDTO,
    CreateUserResponseDTO,
    LoginRequestDTO,
    LoginResponseDTO,
)
from errors import BadRequestError
from fastapi import status, Response


class IUserController(ABC):
    @abstractmethod
    def create(self, request: CreateUserRequestDTO, response: Response) -> CreateUserResponseDTO:
        pass

    @abstractmethod
    def login(self, request: LoginRequestDTO, response: Response) -> LoginResponseDTO:
        pass


class UserController(IUserController):
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    def create(self, request: CreateUserRequestDTO, response: Response) -> CreateUserResponseDTO:
        user = UserModel(
            email=request.email,
            username=request.username,
            password=request.password,
            birthdate=request.birthdate,
        )
        res = self._user_service.create(user)
        response.status_code = status.HTTP_201_CREATED
        return CreateUserResponseDTO(token=res)
    
    def login(self, request: LoginRequestDTO, response: Response) -> LoginResponseDTO:
        if request.email == "" and request.username == "":
            raise BadRequestError("inform email or username to login")
        
        if request.email != "" and request.username != "":
            raise BadRequestError("too many info, inform just one email or username to login")
        
        res = self._user_service.login(request.username, request.email, request.password)
        response.status_code = status.HTTP_200_OK
        return LoginResponseDTO(token=res)