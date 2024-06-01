from pydantic import BaseModel, field_validator
from errors import BadRequestError
from validators import email_validator


class LoginRequestDTO(BaseModel):
    username: str = ""
    email: str = ""
    password: str

class LoginResponseDTO(BaseModel):
    token: str