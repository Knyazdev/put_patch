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


@pytest.fixture(autouse=True, scope='session')
def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(autouse=True, scope='session')
async def async_main(check_test_mode):
    async with engine_null_pull.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    with open('tests/mock_hotels.json') as file:
        hotels = json.load(file)

    with open('tests/mock_rooms.json') as file:
        rooms = json.load(file)

    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        await db.hotels.add_bulk([HotelAdd(**hotel) for hotel in hotels])
        await db.commit()

        await db.rooms.add_bulk([RoomAdd(**room) for room in rooms])
        await db.commit()


@pytest.fixture(autouse=True, scope='session')
async def test_register_user(async_main):
    async with AsyncClient(base_url='http://test', transport=ASGITransport(app=app)) as ac:
        await ac.post('/auth/register', json={
            'email': 'knyaz.dev@gmail.com',
            'password': '123456'
        })
