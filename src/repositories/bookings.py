from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.schemas.booking import Booking
from sqlalchemy import select
from src.repositories.mappers.mappers import BookingDataMapper
from datetime import date


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
