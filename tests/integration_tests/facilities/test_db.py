from src.schemas.facilities import FacilityRequest
from httpx import AsyncClient


async def test_get_facilites(ac: AsyncClient):
    response = await ac.get("/facility")
    assert response.status_code == 200
    print(f"{response.json()=}")


async def test_add_facility(db):
    await db.facilities.add(FacilityRequest(title='Test Request'))
    await db.commit()
