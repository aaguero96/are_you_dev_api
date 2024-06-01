from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, Integer, ForeignKey
from sqlalchemy.sql import expression
from .base_model import BaseModel


class WeightModel(BaseModel):
    __tablename__ = "weights"

    id: Mapped[UUID] = mapped_column(name="id", type_=UUID(as_uuid=True), primary_key=True, server_default=expression.func.uuid_generate_v4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), name="user_id", type_=UUID(as_uuid=True))
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), name="question_id", type_=UUID(as_uuid=True))
    backend: Mapped[Integer] = mapped_column(name="backend", type_=Integer)
    frontend: Mapped[Integer] = mapped_column(name="frontend", type_=Integer)