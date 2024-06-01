from datetime import date, datetime
from pydantic import BaseModel, field_validator, Field
from validators import email_validator, birthdate_validator
from errors import BadRequestError
from utils import password_encode


class CreateUserRequestDTO(BaseModel):
    email: str = Field(example="test@test.com")
    username: str = Field(example="test")
    password: str = Field(example="123456")
    birthdate: date = Field(example="2000-12-31")

    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value:
            raise BadRequestError("field email is required")
        if not email_validator(value):
            raise BadRequestError("email has invalid format")
        return value
    
    @field_validator('birthdate', mode='before')
    @classmethod
    def validate_birthdate(cls, value: str) -> str:
        if not birthdate_validator(value):
            raise BadRequestError("birth date has to be YYYY-MM-DD")
        value_date = datetime.strptime(value, "%Y-%m-%d").date()
        if value_date > datetime.today().date():
            raise BadRequestError("you are not George McFly, try again")
        if datetime.today().date().year - value_date.year > 200:
            raise BadRequestError("you are not Matusalem, try again")
        return value
    
    @field_validator('password', mode='before')
    @classmethod
    def hash_passord(cls, value: str) -> str:
        return password_encode(value)


class CreateUserResponseDTO(BaseModel):
    token: str