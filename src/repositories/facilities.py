from src.repositories.base import BaseRepository
from src.models.facilites import FacilityOrm, RoomFacilitiesOrm
from sqlalchemy import select
from src.schemas.facilities import RoomFacilityRequest
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilityRepository(BaseRepository):
    model = FacilityOrm
    mapper = FacilityDataMapper


class RoomFacilityRepository(BaseRepository):
    model = RoomFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def get_ids(self, room_id: int):
        query = (
            select(self.model.facility_id)
            .select_from(self.model)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, room_id: int, data: list[int] | None = None):
        ids = await self.get_ids(room_id)
        for id in ids:
            if id not in data:
                await self.delete(room_id=room_id, facility_id=id)
        for fid in data:
            if fid not in ids:
                await self.add(RoomFacilityRequest(room_id=room_id, facility_id=fid))
