from abc import ABC, abstractmethod
from infra import IDatabaseConfig
from models import UserModel


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: UserModel) -> None:
        pass


class UserRepository(IUserRepository):
    def __init__(self, database_config: IDatabaseConfig) -> None:
        self._session = database_config.session()

    def create(self, user: UserModel) -> UserModel:
        self._session.add(user)
        self._session.commit()
        return user
        