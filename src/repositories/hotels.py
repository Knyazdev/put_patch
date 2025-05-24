from repositories.base import BaseRepository
from models.hotels import HotelOrm
from sqlalchemy import select, func
from schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelOrm
    scheme = Hotel

    async def get_all(self, location, title, page, offset) -> list[Hotel]:
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
        return [self.scheme.model_validate(item, from_attributes=True) for item in result.scalars().all()]
