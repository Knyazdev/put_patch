from fastapi import APIRouter, Body
from schemas.rooms import RoomAdd, RoomPatch
from database import async_session_maker
from repositories.rooms import RoomRepository


router = APIRouter(tags=['Комнаты'])


@router.get("/hotels/{hotel_id}/rooms")
async def get_items(hotel_id: int):
    async with async_session_maker() as session:
        items = await RoomRepository(session).get_all(hotel_id=hotel_id)
    return {'error': None, 'result': items}


@router.post("/hotels/{hotel_id}")
async def create_hotels_room(hotel_id: int, data: RoomAdd = Body()):
    data.hotel_id = hotel_id
    async with async_session_maker() as session:
        room = await RoomRepository(session).add(data)
        await session.commit()
        return {'error': None, 'result': room}


@router.put("/room/{room_id}")
async def update_by_id(room_id: int, data: RoomAdd = Body()):
    async with async_session_maker() as session:
        await RoomRepository(session).edit(data, id=room_id)
        await session.commit()
        return {'status': 'OK'}


@router.delete("/room/{room_id}")
async def delete_by_id(room_id: int):
    async with async_session_maker() as session:
        await RoomRepository(session).delete(id=room_id)
        await session.commit()
        return {'status': 'OK'}


@router.patch("/room/{room_id}")
async def update_partial(room_id: int, data: RoomPatch = Body()):
    async with async_session_maker() as session:
        await RoomRepository(session).edit(data, id=room_id, exclude_unset=True)
        await session.commit()
        return {'status': 'OK'}


@router.get("/room/{room_id}")
async def get_one_by_id(room_id: int):
    async with async_session_maker() as session:
        data = await RoomRepository(session).get_one_or_none(id=room_id)
        return {'error': None, 'result': data}
