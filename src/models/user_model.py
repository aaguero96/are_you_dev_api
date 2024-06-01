from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID, Date, DateTime
from sqlalchemy.sql import expression
from .base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(name="id", type_=UUID(as_uuid=True), primary_key=True, server_default=expression.func.uuid_generate_v4())
    email: Mapped[str] = mapped_column(name="email", type_=String)
    username: Mapped[str] = mapped_column(name="username", type_=String)
    password: Mapped[str] = mapped_column(name="password", type_=String)
    birthdate: Mapped[Date] = mapped_column(name="birthdate", type_=Date)
    created_at: Mapped[DateTime] = mapped_column(name="created_at", type_=DateTime, server_default=expression.func.now())
    updated_at: Mapped[DateTime] = mapped_column(name="updated_at", type_=DateTime, server_default=expression.func.now())
    deleted_at: Mapped[DateTime] = mapped_column(name="deleted_at", type_=DateTime, nullable=True)