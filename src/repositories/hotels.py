from src.repositories.base import BaseRepository
from src.models.hotels import HotelOrm
from src.models.rooms import RoomsOrm
from sqlalchemy import select, func
from src.schemas.hotels import Hotel
from datetime import date
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper
from src.exceptions import DateFromMoreToException
import logging


class HotelRepository(BaseRepository):
    model = HotelOrm
    mapper = HotelDataMapper

    async def get_all(self, location, title, page, offset) -> list[Hotel]:
        query = select(self.model)
        if location:
            query = query.filter(
                func.lower(self.model.location).contains(location.lower().strip())
            )
        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.lower().strip())
            )
        query = query.limit(offset).offset(offset * (page - 1))
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(item) for item in result.scalars().all()
        ]

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        title: str | None = None,
        location: str | None = None,
        page: int = 1,
        offset: int = 5,
    ) -> list[Hotel]:
        if date_from > date_to:
            logging.info(f"ERR DATE {date_from} > {date_to}")
            raise DateFromMoreToException
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(self.model)
        if location:
            query = query.filter(
                func.lower(self.model.location).contains(location.lower().strip())
            )
        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.lower().strip())
            )
        query = query.filter(self.model.id.in_(hotel_ids_to_get))
        query = query.limit(offset).offset(offset * (page - 1))

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(item) for item in result.scalars().all()
        ]
