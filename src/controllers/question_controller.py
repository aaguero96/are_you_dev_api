from abc import ABC, abstractmethod
from services import IQuestionService
from models import QuestionModel
from dtos import (
    CreateQuestionRequestDTO,
    CreateQuestionResponseDTO,
)
from errors import BadRequestError
from fastapi import status, Response


class IQuestionController(ABC):
    @abstractmethod
    def create(self, request: CreateQuestionRequestDTO, response: Response) -> CreateQuestionResponseDTO:
        pass


class QuestionController(IQuestionController):
    def __init__(self, question_service: IQuestionService) -> None:
        self._question_service = question_service

    def create(self, request: CreateQuestionRequestDTO, response: Response) -> CreateQuestionResponseDTO:
        question = QuestionModel(
            description=request.description,
            adults_only=request.adults_only,
        )
        res = self._question_service.create(question)
        response.status_code = status.HTTP_201_CREATED
        return CreateQuestionResponseDTO(
            id=str(res.id),
            description=res.description,
        )