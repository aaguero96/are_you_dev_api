from abc import ABC, abstractmethod
from repositories import IUserRepository
from models import UserModel
from utils import encode_data


class IUserService(ABC):
    @abstractmethod
    def create(self, user: UserModel) -> str:
        pass


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    def create(self, user: UserModel) -> str:
        response = self._user_repository.create(user)
        return encode_data({
            "id": str(response.id),
            "username": response.username,
        })
        