from pydantic import BaseModel, Field
from validators import email_validator


class LoginRequestDTO(BaseModel):
    email: str = ""
    username: str = ""
    password: str


class LoginResponseDTO(BaseModel):
    token: str