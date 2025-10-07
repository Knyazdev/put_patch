
from unittest import mock

mock.patch("fastapi_cache.decorator.cache",
           lambda *a, **kw: (lambda f: f)).start()
import pytest
from src.database import Base, engine_null_pull, async_session_maker_null_pull
from src.models import *
from src.config import settings
from src.main import app
from httpx import AsyncClient, ASGITransport
import json
from src.utils.db_manager import DBManager
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.api.dependencies import get_db



@pytest.fixture(autouse=True, scope='session')
def check_test_mode():
    assert settings.MODE == 'TEST'


async def get_db_null_pull() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(autouse=True, scope='session')
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    with open('tests/mock_hotels.json') as file:
        hotels = json.load(file)

    with open('tests/mock_rooms.json') as file:
        rooms = json.load(file)

    async with DBManager(session_factory=async_session_maker_null_pull) as _db:
        await _db.hotels.add_bulk([HotelAdd(**hotel) for hotel in hotels])
        await _db.rooms.add_bulk([RoomAdd(**room) for room in rooms])
        await _db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(base_url='http://test', transport=ASGITransport(app=app)) as ac:
        yield ac


@pytest.fixture(autouse=True, scope='session')
async def test_register_user(setup_database, ac):
    await ac.post('/auth/register', json={
        'email': 'knyaz.dev@gmail.com',
        'password': '123456'
    })

@pytest.fixture(scope='session')
async def authenticated_ac(test_register_user, ac):
    response = await ac.post("/auth/login", json={
        'email':'knyaz.dev@gmail.com',
        'password':'123456'
    })
    assert response
    assert response.status_code == 200
    # print(f"{response.cookies}")
    assert response.cookies['access_token']
    yield ac
