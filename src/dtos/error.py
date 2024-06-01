from pydantic import BaseModel

class ErrorResponseDTO(BaseModel):
    message: str