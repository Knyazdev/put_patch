from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    scheme: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.scheme.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        if result:
            return self.scheme.model_validate(result.scalar_one_or_none(), from_attributes=True)
        return None

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(
            **data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalars().one(), from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        stmt = (
            update(self.model)
            .values(
                **data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
