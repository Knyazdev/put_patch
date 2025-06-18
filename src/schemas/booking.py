from pydantic import BaseModel
from datetime import date
from models.bookings import BookingOrm


class BookingRequest(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class BookingAdd(BookingRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
