from repositories.base import BaseRepository
from models.bookings import BookingOrm
from schemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingOrm
    scheme = Booking
