from fastapi import APIRouter, Body, Query
from src.schemas.rooms import  RoomRequest, RoomPatchRequest
from .dependencies import DBDep
from datetime import date
from src.exceptions import (
    RoomNotFoundException,
    HotelNotFoundException,
    HttpHotelNotFoundException,
    HttpRoomNotFoundException,
    InccorectFacilityException,
    HttpInccorectFacilityException
)
from src.services.rooms import RoomService
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_items(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-12-01"),
    date_to: date = Query(example="2025-07-01"),
):
    try:
        return {
            "error": None, 
            "result": await RoomService(db).items(
                hotel_id=hotel_id, 
                date_from=date_from, 
                date_to=date_to
            )}
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex


@router.post("/{hotel_id}/rooms")
async def create_hotels_room(db: DBDep, hotel_id: int, data: RoomRequest = Body()):
    try:
        await HotelService(db).get_one(hotel_id)
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex
    try:    
        return {
            "error": None, 
            "result": await RoomService(db).add(
                hotel_id=hotel_id, 
                data=data
            )
        }
    except InccorectFacilityException as ex:
        raise HttpInccorectFacilityException from ex


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_by_id(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    data: RoomRequest = Body()
):
    try:
        await RoomService(db).get_one(
            room_id=room_id, 
            hotel_id=hotel_id
        )

        await RoomService(db).edit(
            hotel_id=hotel_id, 
            room_id=room_id, 
            data=data
        )
    except RoomNotFoundException as ex:
        raise HttpRoomNotFoundException from ex
    except InccorectFacilityException as ex:
        raise HttpInccorectFacilityException from ex

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_by_id(
    db: DBDep, 
    hotel_id: int, 
    room_id: int
):
    try:
        await RoomService(db).get_one(
            room_id=room_id, 
            hotel_id=hotel_id
        )
    except RoomNotFoundException as ex:
        raise HttpRoomNotFoundException from ex
    await RoomService(db).delete(
        hotel_id=hotel_id, 
        room_id=room_id
    )
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_partial(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    data: RoomPatchRequest = Body()
):
    try:
        await RoomService(db).get_one(
            room_id=room_id, 
            hotel_id=hotel_id
        )

        await RoomService(db).update_partial(
            room_id=room_id, 
            hotel_id=hotel_id, 
            data=data
        )
    except RoomNotFoundException as ex:
        raise HttpRoomNotFoundException from ex
    except InccorectFacilityException as ex:
        raise HttpInccorectFacilityException from ex
    return {"status": "OK"}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_by_id(
    db: DBDep, 
    hotel_id: int, 
    room_id: int
):
    try:
        return {
            "error": None, 
            "result": await RoomService(db).get_one(
                room_id=room_id, 
                hotel_id=hotel_id
            )
        }
    except RoomNotFoundException as ex:
        raise HttpRoomNotFoundException from ex
