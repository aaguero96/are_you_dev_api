from fastapi import APIRouter, Response, status, Depends
from dtos import (
    CreateQuestionRequestDTO,
    CreateQuestionResponseDTO,
    ErrorResponseDTO,
)
from controllers import IQuestionController
from errors import HttpError
from middlewares import IAuthMiddleware


class QuestionRoute:
    def __init__(self, question_controller: IQuestionController, auth_middleware: IAuthMiddleware) -> None:
        self.router = APIRouter(prefix="/question")
        self._question_controller = question_controller
        self._auth_middleware = auth_middleware
        self.setup_routes()

    def setup_routes(self):
        @self.router.post(
            "/",
            dependencies=[Depends(self._auth_middleware.session)],
            response_model=CreateQuestionResponseDTO | ErrorResponseDTO,
            tags=["question"],
            summary="Create question",
            responses={
                status.HTTP_201_CREATED: {"model": CreateQuestionResponseDTO, "description": "success"},
                status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseDTO, "description": "unauthorized"},
                status.HTTP_403_FORBIDDEN: {"model": ErrorResponseDTO, "description": "forbidden"},
                status.HTTP_409_CONFLICT: {"model": ErrorResponseDTO, "description": "conflict"},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponseDTO, "description": "internal server error"}
            },
        )
        def create(request: CreateQuestionRequestDTO, response: Response):
            return self._question_controller.create(request, response)