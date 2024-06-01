from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from abc import ABC, abstractmethod
from models import BaseModel
from .env_config import IEnvConfig


class IDatabaseConfig(ABC):
    @abstractmethod
    def session(self) -> Session:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass


class DatabaseConfig(IDatabaseConfig):
    def __init__(self, env_config: IEnvConfig) -> None:
        user = env_config.get_env("DATABASE_USER")
        password = env_config.get_env("DATABASE_PASSWORD")
        database_name = env_config.get_env("DATABASE_NAME")
        port = env_config.get_env("DATABASE_PORT")
        host = env_config.get_env("DATABASE_HOST")

        databaseUrl = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}"
        engine = create_engine(databaseUrl, echo=True)
        session = sessionmaker(bind=engine)

        self._engine = engine
        self._session = session()
    
    def session(self) -> Session:
        return self._session
        
    def create_tables(self) -> None:
        BaseModel.metadata.create_all(bind=self._engine)
