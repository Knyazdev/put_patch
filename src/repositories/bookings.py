from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.schemas.booking import Booking
from sqlalchemy import select
from src.repositories.mappers.mappers import BookingDataMapper
from datetime import date
from src.schemas.hotels import HotelAdd
from src.repositories.utils import rooms_ids_for_booking
from fastapi import HTTPException


class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper

    async def get_mine(self, user_id) -> list[Booking]:
        query = select(self.model)
        query = query.filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(item) for item in result.scalars().all()
        ]

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_booking(self, data: HotelAdd, hotel_id: int):
        room_ids = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        query = await self.session.execute(room_ids)
        rooms: list[int] = query.scalars().all()
        if data.room_id not in rooms:
            raise HTTPException(500)

        return await self.add(data)
