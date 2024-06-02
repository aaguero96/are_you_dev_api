from pydantic import BaseModel, Field


class CreateQuestionRequestDTO(BaseModel):
    description: str = Field(example="do you have a girlfriend?")
    adults_only: bool = Field(example=False)


class CreateQuestionResponseDTO(BaseModel):
    id: str
    description: str