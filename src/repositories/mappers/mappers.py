from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelOrm
from src.schemas.hotels import Hotel

from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRels

from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword

from src.models.bookings import BookingOrm
from src.schemas.booking import Booking

from src.models.facilites import FacilityOrm, RoomFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility


class HotelDataMapper(DataMapper):
    db_model = HotelOrm
    scheme = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    scheme = Room


class RoomRelDataMapper(DataMapper):
    db_model = RoomsOrm
    scheme = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    scheme = User


class UserDataWithHashMapper(DataMapper):
    db_model = UsersOrm
    scheme = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingOrm
    scheme = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilityOrm
    scheme = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomFacilitiesOrm
    scheme = RoomFacility
