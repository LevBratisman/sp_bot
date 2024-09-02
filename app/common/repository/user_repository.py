from sqlalchemy import insert, select
from app.common.repository.crud_base_repository import CRUDBase
from app.common.models.user import User

from app.db.session import async_session

class UserRepository(CRUDBase):
    model = User

    @classmethod
    async def add(cls, *, telegram_id: int, username: str | None):
        async with async_session() as session:
            pre_query = select(cls.model).where(telegram_id == telegram_id)
            user = await session.execute(pre_query)
            if not user.scalar_one_or_none():
                query = insert(cls.model).values(telegram_id=telegram_id, username=username)
                await session.execute(query)
                await session.commit()