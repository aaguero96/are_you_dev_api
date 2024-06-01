from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os


class IEnvConfig(ABC):
    def get_env(key : str) -> str:
        pass


class EnvConfig(IEnvConfig):
    def __init__(self) -> None:
        load_dotenv()

    def get_env(self, key : str) -> str:
        return os.getenv(key)