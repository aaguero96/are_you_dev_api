from datetime import date
from pydantic import BaseModel, field_validator
from validators import email_validator
from errors import BadRequestError
from utils import password_encode


class CreateUserRequestDTO(BaseModel):
    email: str
    username: str
    password: str
    birthdate: date

    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if email_validator(value):
            return value
        raise BadRequestError("email is invalid")
    
    @field_validator('password', mode='before')
    @classmethod
    def hash_passord(cls, value: str) -> str:
        return password_encode(value)


class CreateUserResponseDTO(BaseModel):
    token: str