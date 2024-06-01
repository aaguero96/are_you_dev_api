from abc import ABC, abstractmethod
from repositories import IUserRepository
from models import UserModel
from infra import IJwtConfig
from utils import password_compare
from errors import UnauthorizedError


class IUserService(ABC):
    @abstractmethod
    def create(self, user: UserModel) -> str:
        pass

    @abstractmethod
    def login(self, username: str, email: str, password: str) -> str:
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
        
    def login(self, username: str, email: str, password: str) -> str:
        user = UserModel()

        if username:
            user = self._user_repository.get_by_username(username)
        elif email:
            user = self._user_repository.get_by_email(email)

        if not password_compare(password, user.password):
            raise UnauthorizedError("invalid credentials")
        
        return self._jwt_config.encode_data({
            "id": str(user.id),
            "username": user.username,
        })