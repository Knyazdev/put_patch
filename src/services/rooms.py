from src.services.base import BaseService
from datetime import date
from src.schemas.rooms import (
    RoomRequest, 
    RoomAdd, 
    RoomPatchRequest,
    RoomPatch
)
from src.schemas.facilities import RoomFacilityRequest
from src.exceptions import (
    check_date_to_after_date_from,
    RecordNotFoundException,
    HotelNotFoundException,
    InccorectFacilityException,
    RoomNotFoundException
)
class RoomService(BaseService):
    async def items(
            self,
            hotel_id:int,
            date_from:date,
            date_to:date,
    ):
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except RecordNotFoundException as ex:
            raise HotelNotFoundException from ex
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    
    async def add(self, hotel_id: int, data: RoomRequest):
        item = await self.db.rooms.add(
            RoomAdd(hotel_id=hotel_id, **data.model_dump(exclude={"facility_ids"}))
        )
        li = [
            RoomFacilityRequest(room_id=item.id, facility_id=fid)
            for fid in data.facility_ids
        ]
        if li:
            if not await self.db.facilities.check_aviable(data.facility_ids):
                self.db.rollback()
                raise InccorectFacilityException
            await self.db.rooms_facilities.add_bulk(li)

        await self.db.commit()
        return item
    
    async def edit(
            self, 
            hotel_id: int, 
            room_id: int, data: RoomRequest
    ):
        if not await self.db.facilities.check_aviable(data.facility_ids):
            raise InccorectFacilityException
        
        await self.db.rooms.edit(RoomAdd(
            hotel_id=hotel_id, 
            **data.model_dump()
        ), id=room_id)
        await self.db.rooms_facilities.update(
            room_id=room_id, 
            data=data.facility_ids
        )
        await self.db.commit()

    async def delete(self, hotel_id: int, room_id: int):
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.delete(room_id=room_id)
        await self.db.commit()

    async def update_partial(
            self, hotel_id: int, 
            room_id: int, 
            data: RoomPatchRequest
        ):
        if not await self.db.facilities.check_aviable(data.facility_ids):
            raise InccorectFacilityException
        room_data_dict = data.model_dump(exclude_unset=True)
        dat = RoomPatch(hotel_id=hotel_id, id=room_id, **room_data_dict)
        await self.db.rooms.edit(dat, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        if "facility_ids" in room_data_dict:
            await self.db.rooms_facilities.update(room_id=room_id, data=data.facility_ids)
        await self.db.commit()

    async def get_one(self, hotel_id: int, room_id: int):
        try:
            return await self.db.rooms.get_one(
                id=room_id, 
                hotel_id=hotel_id
            )
        except RecordNotFoundException as ex:
            raise RoomNotFoundException from ex
