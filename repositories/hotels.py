from repositories.base import BaseRepository
from src.models.hotels import HotelOrm
from sqlalchemy import select, func


class HotelRepository(BaseRepository):
    model = HotelOrm

    async def get_all(self, location, title, page, offset):
        query = select(HotelOrm)
        if location:
            query = query.filter(func.lower(
                HotelOrm.location).contains(location.lower().strip()))
        if title:
            query = query.filter(func.lower(
                HotelOrm.title).contains(title.lower().strip()))
        query = (
            query
            .limit(offset)
            .offset(offset*(page - 1))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, **data):
        return await super().add(**data)
