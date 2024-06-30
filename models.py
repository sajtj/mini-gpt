from sqlalchemy import ForeignKey, Integer
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base) :
    __tablename__ =  "users"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    username : Mapped[str] = mapped_column(unique=True, index=True)


class Query(Base) :
    __tablename__ =  "queries"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    prompt : Mapped[str] = mapped_column(index=True)
    response : Mapped[str] = mapped_column()
    tokens : Mapped[int] = mapped_column()
    llm_name : Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    