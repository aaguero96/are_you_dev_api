from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UUID, Boolean
from sqlalchemy.sql import expression
from .base_model import BaseModel


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    id: Mapped[UUID] = mapped_column(name="id", type_=UUID(as_uuid=True), primary_key=True, server_default=expression.func.uuid_generate_v4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), name="user_id", type_=UUID(as_uuid=True))
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), name="question_id", type_=UUID(as_uuid=True))
    answer: Mapped[Boolean]= mapped_column(name="answer", type_=Boolean)
