from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID, Boolean, DateTime
from sqlalchemy.sql import expression
from .base_model import BaseModel


class QuestionModel(BaseModel):
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(name="id", type_=UUID(as_uuid=True), primary_key=True, server_default=expression.func.uuid_generate_v4())
    description: Mapped[str] = mapped_column(name="description", type_=String)
    adults_only: Mapped[str] = mapped_column(name="adults_only", type_=Boolean)
    created_at: Mapped[DateTime] = mapped_column(name="created_at", type_=DateTime, server_default=expression.func.now())
    updated_at: Mapped[DateTime] = mapped_column(name="updated_at", type_=DateTime, server_default=expression.func.now())
    deleted_at: Mapped[DateTime] = mapped_column(name="deleted_at", type_=DateTime, nullable=True)

    