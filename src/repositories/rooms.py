from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from sqlalchemy import select, func
from datetime import date
from src.repositories.bookings import BookingOrm
from src.repositories.utils import rooms_ids_for_booking


class RoomRepository(BaseRepository):
    model = RoomsOrm
    scheme = Room

    async def get_all(self, hotel_id) -> list[Room]:
        query = select(self.model)
        query = query.filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.scheme.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ) -> list[Room]:
        return await self.get_filtered(self.model.id.in_(rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to)))
