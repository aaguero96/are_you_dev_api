from abc import ABC, abstractmethod
from repositories import IUserRepository
from models import UserModel
from infra import IJwtConfig


class IUserService(ABC):
    @abstractmethod
    def create(self, user: UserModel) -> str:
        pass


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, jwt_config: IJwtConfig) -> None:
        self._user_repository = user_repository
        self._jwt_config = jwt_config

    def create(self, user: UserModel) -> str:
        response = self._user_repository.create(user)
        return self._jwt_config.encode_data({
            "id": str(response.id),
            "username": response.username,
        })
        