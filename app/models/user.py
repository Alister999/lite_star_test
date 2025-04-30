from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    surname: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]