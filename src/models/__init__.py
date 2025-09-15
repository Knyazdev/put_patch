from src.database import Base

# Импортируем все модели, чтобы они регистрировались в Base.metadata
from .hotels import HotelOrm
from .rooms import RoomsOrm
from .users import UsersOrm
from .bookings import BookingOrm
from .facilites import FacilityOrm, RoomFacilitiesOrm

__all__ = [
    "HotelOrm",
    "RoomsOrm",
    "UsersOrm",
    "BookingOrm",
    "FacilityOrm",
    "RoomFacilitiesOrm",
]
