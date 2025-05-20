from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(
            **data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, cri) -> None:
        stmt = update(self.model).values(
            **data.model_dump()).where(*[getattr(self.model, k) == v for k, v in cri.items()])
        await self.session.execute(stmt)

    async def delete(self, cri) -> None:
        stmt = delete(self.model).where(
            *[getattr(self.model, k) == v for k, v in cri.items()])
        await self.session.execute(stmt)
