from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from abc import ABC, abstractmethod
from models import BaseModel


class IDatabaseConfig(ABC):
    @abstractmethod
    def session(self) -> Session:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass


class DatabaseConfig(IDatabaseConfig):
    def __init__(self) -> None:
        databaseUrl = f"postgresql+psycopg2://admin:admin@localhost:5432/test"
        engine = create_engine(databaseUrl, echo=True)
        session = sessionmaker(bind=engine)

        self._engine = engine
        self._session = session()
    
    def session(self) -> Session:
        return self._session
        
    def create_tables(self) -> None:
        BaseModel.metadata.create_all(bind=self._engine)
