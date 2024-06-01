from abc import ABC, abstractmethod
from services import IUserService
from models import UserModel
from dtos import CreateUserRequestDTO, CreateUserResponseDTO


class IUserController(ABC):
    @abstractmethod
    def create(self, request: CreateUserRequestDTO) -> CreateUserResponseDTO:
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