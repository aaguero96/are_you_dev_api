from fastapi import APIRouter, Response, status
from dtos import (
    CreateQuestionRequestDTO,
    CreateQuestionResponseDTO,
    ErrorResponseDTO,
)
from controllers import IQuestionController
from errors import HttpError


class QuestionRoute:
    def __init__(self, question_controller: IQuestionController) -> None:
        self.router = APIRouter(prefix="/question")
        self._question_controller = question_controller
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/", response_model=CreateQuestionResponseDTO | ErrorResponseDTO)
        def create(request: CreateQuestionRequestDTO, response: Response):
            return self._question_controller.create(request, response)