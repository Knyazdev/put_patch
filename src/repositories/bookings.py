from repositories.base import BaseRepository
from models.bookings import BookingOrm
from schemas.booking import Booking
from sqlalchemy import select


class BookingRepository(BaseRepository):
    model = BookingOrm
    scheme = Booking

    async def get_mine(self, user_id) -> list[Booking]:
        query = select(self.model)
        query = query.filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [self.scheme.model_validate(item, from_attributes=True) for item in result.scalars().all()]
