from abc import ABC, abstractmethod
from .env_config import IEnvConfig
import datetime
import jwt


class IJwtConfig(ABC):
    @abstractmethod
    def encode_data(self, payload) -> str:
        pass


class JwtConfig(IJwtConfig):
    def __init__(self, env_config: IEnvConfig) -> None:
        self._env_config = env_config

    def encode_data(self, payload) -> str:
        secret = self._env_config.get_env("JWT_SECRET")
        expires_in = self._env_config.get_env("JWT_EXPIRES_IN")

        payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=int(expires_in))

        return jwt.encode(payload, secret, algorithm='HS256')