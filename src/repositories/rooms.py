from repositories.base import BaseRepository
from models.rooms import RoomsOrm
from schemas.rooms import Room
from sqlalchemy import select


class RoomRepository(BaseRepository):
    model = RoomsOrm
    scheme = Room

    async def get_all(self, hotel_id) -> list[Room]:
        query = select(self.model)
        query = query.filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.scheme.model_validate(item, from_attributes=True) for item in result.scalars().all()]
