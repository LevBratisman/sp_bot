from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from typing import Optional

from app.db.base_class import Base


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column()