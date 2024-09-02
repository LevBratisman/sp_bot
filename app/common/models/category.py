from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Category(Base):
    name: Mapped[str] = mapped_column()