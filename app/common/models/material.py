from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base_class import Base


class Material(Base):
    name: Mapped[str] = mapped_column()
    file: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete='CASCADE'))