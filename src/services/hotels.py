from src.services.base import BaseService
from datetime import date
from src.schemas.hotels import HotelAdd
from src.exceptions import (
    RecordNotFoundException, 
    HotelNotFoundException,
    check_date_to_after_date_from
)

class HotelService(BaseService):
    async def get_filtered_by_time(
        self, 
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date
    ):
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            offset=per_page,
            page=pagination.page,
            title=title,
            location=location,
        )
    
    async def delete(self, id:int):
        try:
            await self.db.hotels.get_one(id=id)
        except RecordNotFoundException as ex:
            raise HotelNotFoundException from ex
        await self.db.hotels.delete(id=id)
        await self.db.commit()
    
    async def add(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit(self, hotel_id: int, hotel_data: HotelAdd, exclude=False):
        try:
            await self.get_one(id=hotel_id)
        except RecordNotFoundException as e:
            raise HotelNotFoundException from e
        await self.db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=exclude)
        await self.db.commit()

    async def get_one(self, id:int):
        try:
            return await self.db.hotels.get_one(id=id)
        except RecordNotFoundException as ex:
            raise HotelNotFoundException from ex