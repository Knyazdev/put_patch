from fastapi import APIRouter, Body
from schemas.rooms import RoomAdd, RoomPatch, RoomRequest
from .dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=['Комнаты'])


@router.get("/{hotel_id}/rooms")
async def get_items(
    db: DBDep,
    hotel_id: int
):
    items = await db.rooms.get_all(hotel_id=hotel_id)
    return {'error': None, 'result': items}


@router.post("/{hotel_id}/rooms")
async def create_hotels_room(
    db: DBDep,
    hotel_id: int,
    data: RoomRequest = Body()
):
    room = await db.rooms.add(RoomAdd(hotel_id=hotel_id, **data.model_dump()))
    await db.commit()
    return {'error': None, 'result': room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomRequest = Body()
):
    await db.rooms.edit(RoomAdd(hotel_id=hotel_id, **data.model_dump()), id=room_id)
    await db.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_partial(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomPatch = Body()
):
    await db.rooms.edit(data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    await db.commit()
    return {'status': 'OK'}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    data = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return {'error': None, 'result': data}
