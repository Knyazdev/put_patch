from repositories.hotels import HotelRepository
from repositories.rooms import RoomRepository
from repositories.users import UserRepository
from repositories.bookings import BookingRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def session_factory():
        ...

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.users = UserRepository(self.session)
        self.booking = BookingRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
