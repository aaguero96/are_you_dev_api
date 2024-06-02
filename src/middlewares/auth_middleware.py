from abc import ABC, abstractmethod
from fastapi import status, Depends, Request
from errors import UnauthorizedError, BadRequestError, ForbiddenError
from infra import IJwtConfig
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from repositories import IUserRepository


bearer_token_scheme = HTTPBearer(scheme_name="Bearer", description="authorization")


class IAuthMiddleware(ABC):
    def session(self, request: Request):
        pass


class AuthMiddleware(IAuthMiddleware):
    def __init__(self, jwt_config: IJwtConfig, user_repository: IUserRepository) -> None:
        self._jwt_config = jwt_config
        self._user_repository = user_repository

    def session(self, token: HTTPAuthorizationCredentials = Depends(bearer_token_scheme)):   
        data = self._jwt_config.decode_data(token.credentials)

        user_id = data["id"]
        username = data["username"]

        user = self._user_repository.get_by_username(username)
        if str(user.id) != user_id:
            UnauthorizedError("user has been deleted")
        
        return user
