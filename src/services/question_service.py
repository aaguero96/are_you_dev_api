from abc import ABC, abstractmethod
from repositories import IQuestionRepository
from models import QuestionModel
from utils import password_compare
from errors import UnauthorizedError
from external_services import IOpenAiService


class IQuestionService(ABC):
    @abstractmethod
    def create(self, question: QuestionModel) -> QuestionModel:
        pass


class QuestionService(IQuestionService):
    def __init__(self, question_repository: IQuestionRepository, openai_service: IOpenAiService) -> None:
        self._question_repository = question_repository
        self._openai_service = openai_service

    def create(self, question: QuestionModel) -> QuestionModel:
        existing_questions_json = self._question_repository.get_all_json()
        new_question = self._openai_service.validate_question(question.description, existing_questions_json)
        return self._question_repository.create(QuestionModel(
            description=new_question,
            adults_only=question.adults_only,
        ))