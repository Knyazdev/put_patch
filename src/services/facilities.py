from src.services.base import BaseService
from src.schemas.facilities import (
    Facility,
    FacilityRequest
)
from src.tasks.tasks import test_task

class FacilityService(BaseService):
    async def items(self) -> list[Facility]:
        return await self.db.facilities.get_all()
    
    async def add(self, request: FacilityRequest) -> Facility:
        item = await self.db.facilities.add(request)
        await self.db.commit()

        test_task.delay()
        return item