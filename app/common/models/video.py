from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base_class import Base


class Video(Base):
    name: Mapped[str] = mapped_column()
    file: Mapped[str] = mapped_column()
    caption: Mapped[str] = mapped_column()