from src.services.base import BaseService
from src.schemas.booking import (
    BookingRequest,
    BookingAdd,
    Booking
)
from src.exceptions import (
    RecordNotFoundException,
    RoomNotFoundException
)


class BookingService(BaseService):
    async def add(
            self,
            user_id:int,
            req: BookingRequest
    ) -> Booking:
        try:
            room = await self.db.rooms.get_one(id=req.room_id)
        except RecordNotFoundException as ex:
            raise RoomNotFoundException from ex
        
        data = BookingAdd(
            user_id=user_id, 
            price=room.price, 
            **req.model_dump()
        )
        booking = await self.db.booking.add_booking(
            data, 
            hotel_id=room.hotel_id
        )
        await self.db.commit()
        return booking
    
    async def get_all(self) -> list[Booking]:
        return await self.db.booking.get_all()
    
    async def get_me(self, user_id:int) -> list[Booking]:
        return await self.db.booking.get_mine(user_id)