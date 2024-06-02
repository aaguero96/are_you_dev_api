from abc import ABC, abstractmethod
from infra import IDatabaseConfig
from models import QuestionModel
from sqlalchemy import select, insert
from sqlalchemy.sql import text
from sqlalchemy.exc import NoResultFound, IntegrityError
from errors import NotFoundError, ConflictError
import json


class IQuestionRepository(ABC):
    @abstractmethod
    def create(self, question: QuestionModel) -> QuestionModel:
        pass

    @abstractmethod
    def get_all_json(self) -> str:
        pass

    @abstractmethod
    def is_question_exist(self, description: str) -> bool:
        pass


class QuestionRepository(IQuestionRepository):
    def __init__(self, database_config: IDatabaseConfig) -> None:
        self._session = database_config.session()

    def create(self, question: QuestionModel) -> QuestionModel:
        try:
            response = self._session.execute(
                insert(QuestionModel).values({
                    "description": question.description,
                    "adults_only": question.adults_only,
                }).returning(QuestionModel)
            )
            self._session.commit()
            created_question = response.fetchone()
            return created_question[0]
        except ValueError as err:
            self._session.rollback()
            raise err
        
    def get_all_json(self) -> str:
        try:
            query = text("""
                    SELECT json_agg(row_to_json(sub)) AS json_date FROM (
                        SELECT description FROM questions
                    ) sub
                """)
            response = self._session.execute(query).one()
            return str(response[0])
        except ValueError as err:
            raise err
        
    def is_question_exist(self, description: str) -> bool:
        try:
            query = text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM questions
                    WHERE description = :description
                );  
            """)
            query_params = {"description": description}
            response = self._session.execute(query, query_params).one()
            return response[0] == True
        except ValueError as err:
            raise err