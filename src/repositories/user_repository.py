from abc import ABC, abstractmethod
from infra import IDatabaseConfig
from models import UserModel
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound, IntegrityError
from errors import NotFoundError, ConflictError
from datetime import datetime


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
        try:
            response = self._session.execute(
                insert(UserModel).values({
                    "email": user.email,
                    "username": user.username,
                    "password": user.password,
                    "birthdate": user.birthdate,
                }).returning(UserModel)
            )
            self._session.commit()
            created_user = response.fetchone()
            return created_user[0]
        except IntegrityError as err:
            self._session.rollback()
            if 'unique constraint' in str(err.orig):
                raise ConflictError("user has already been created", err)
            raise err
        except ValueError as err:
            self._session.rollback()
            raise err

    def get_by_username(self, username: str) -> UserModel:
        try:
            response = self._session.execute(
                select(UserModel).where(UserModel.username == username).where(UserModel.deleted_at.is_(None))
            ).one()
            return response[0]
        except NoResultFound as err:
            raise NotFoundError("user not found", err)
    
    def get_by_email(self, email: str) -> UserModel:
        try:
            response = self._session.execute(
                select(UserModel).where(UserModel.email == email).where(UserModel.deleted_at.is_(None))
            ).one()
            return response[0]
        except NoResultFound as err:
            raise NotFoundError("user not found", err)
        