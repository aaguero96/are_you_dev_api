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


class IUserController(ABC):
    @abstractmethod
    def create(self, request: CreateUserRequestDTO) -> CreateUserResponseDTO:
        pass

    @abstractmethod
    def login(self, request: LoginRequestDTO) -> LoginResponseDTO:
        pass


class UserController(IUserController):
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    def create(self, request: CreateUserRequestDTO) -> CreateUserResponseDTO:
        user = UserModel(
            email=request.email,
            username=request.username,
            password=request.password,
            birthdate=request.birthdate,
        )
        response = self._user_service.create(user)
        return CreateUserResponseDTO(token=response)
    
    def login(self, request: LoginRequestDTO) -> LoginResponseDTO:
        if request.email == "" and request.username == "":
            raise BadRequestError("inform email or username to login")
        
        if request.email != "" and request.username != "":
            raise BadRequestError("too many info, inform just one email or username to login")
        
        response = self._user_service.login(request.username, request.email, request.password)
        return LoginResponseDTO(token=response)