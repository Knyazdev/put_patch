from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    role: Mapped[int] = mapped_column(default=0)
