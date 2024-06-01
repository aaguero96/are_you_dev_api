from abc import ABC, abstractmethod
from infra import IDatabaseConfig
from models import UserModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from errors import NotFoundError


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: UserModel) -> None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserModel:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserModel:
        pass


class UserRepository(IUserRepository):
    def __init__(self, database_config: IDatabaseConfig) -> None:
        self._session = database_config.session()

    def create(self, user: UserModel) -> UserModel:
        self._session.add(user)
        self._session.commit()
        return user

    def get_by_username(self, username: str) -> UserModel:
        try:
            response = self._session.execute(
                select(UserModel).where(UserModel.username == username)
            ).one()
            return response[0]
        except NoResultFound as err:
            raise NotFoundError("user not found", err)
    
    def get_by_email(self, email: str) -> UserModel:
        try:
            response = self._session.execute(
                select(UserModel).where(UserModel.email == email)
            ).one()
            return response[0]
        except NoResultFound as err:
            raise NotFoundError("user not found", err)
        