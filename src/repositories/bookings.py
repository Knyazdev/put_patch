from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.schemas.booking import Booking
from sqlalchemy import select
from src.repositories.mappers.mappers import BookingDataMapper
from datetime import date
from pydantic import BaseModel
from src.repositories.utils import rooms_ids_for_booking
from fastapi import HTTPException



class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper

    async def get_mine(self, user_id) -> list[Booking]:
        query = select(self.model)
        query = query.filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BaseModel):
        room_ids = rooms_ids_for_booking(date_from=data.date_from, date_to=data.date_to)
        rooms = await self.get_filtered(self.model.room_id.in_(room_ids))
        isset = False
        for room in rooms:
            if room.room_id == data.room_id:
                isset = True
                break

        if not isset:
            raise HTTPException(status_code=404, detail="Order not found")
        return await self.add(data)