from abc import ABC, abstractmethod
from .env_config import IEnvConfig
import datetime
import jwt
from errors import ForbiddenError, UnauthorizedError


class IJwtConfig(ABC):
    @abstractmethod
    def encode_data(self, payload) -> str:
        pass

    @abstractmethod
    def decode_data(self, token: str):
        pass


class JwtConfig(IJwtConfig):
    def __init__(self, env_config: IEnvConfig) -> None:
        secret = env_config.get_env("JWT_SECRET")
        expires_in = env_config.get_env("JWT_EXPIRES_IN")
        
        self._secret = secret
        self._expires_in = expires_in

    def encode_data(self, payload) -> str:
        payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=int(self._expires_in))

        return jwt.encode(payload, self._secret, algorithm='HS256')
    
    def decode_data(self, token: str):
        try:
            return jwt.decode(token, self._secret, algorithms='HS256')
        except jwt.ExpiredSignatureError as err:
            raise ForbiddenError("token has expired", err)
        except jwt.DecodeError as err:
            raise UnauthorizedError("token is invalid", err)
        except jwt.InvalidTokenError as err:
            raise UnauthorizedError("token is invalid", err)
        except ValueError as err:
            raise err