from fastapi import APIRouter, Body, Query
from src.schemas.rooms import RoomAdd, RoomPatch, RoomRequest, RoomPatchRequest
from src.schemas.facilities import RoomFacilityRequest
from .dependencies import DBDep
from datetime import date


router = APIRouter(prefix="/hotels", tags=['Комнаты'])


@router.get("/{hotel_id}/rooms")
async def get_items(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-12-01"),
    date_to: date = Query(example="2025-07-01")
):
    items = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return {'error': None, 'result': items}


@router.post("/{hotel_id}/rooms")
async def create_hotels_room(
    db: DBDep,
    hotel_id: int,
    data: RoomRequest = Body()
):
    room = await db.rooms.add(RoomAdd(hotel_id=hotel_id, **data.model_dump(exclude={'facility_ids'})))
    li = [RoomFacilityRequest(room_id=room.id, facility_id=fid)
          for fid in data.facility_ids]
    await db.rooms_facilities.add_bulk(li)
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
    await db.rooms_facilities.update(room_id=room_id, data=data.facility_ids)
    await db.commit()
    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_by_id(
    db: DBDep,
    hotel_id: int,
    room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.delete(room_id=room_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_partial(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest = Body()
):
    room_data_dict = data.model_dump(exclude_unset=True)
    dat = RoomPatch(hotel_id=hotel_id, id=room_id, **room_data_dict)
    await db.rooms.edit(dat, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    if 'facility_ids' in room_data_dict:
        await db.rooms_facilities.update(room_id=room_id, data=data.facility_ids)
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
