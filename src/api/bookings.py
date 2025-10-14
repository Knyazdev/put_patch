from fastapi import APIRouter, Body, HTTPException
from src.schemas.booking import BookingRequest, BookingAdd
from .dependencies import DBDep, userIdDep
from src.exceptions import (
    RoomNotFoundException,
    HttpRoomNotFoundException
)
from src.services.bookings import BookingService


router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.post("")
async def create_booking(
    db: DBDep, 
    user_id: userIdDep, 
    req: BookingRequest = Body()
):
    try:
        return {
            'status': 'OK',
            'data': await BookingService(db).add(
                user_id=user_id, 
                req=req
            )
        }
    except RoomNotFoundException as ex:
        raise HttpRoomNotFoundException from ex


@router.get("")
async def get_all(db: DBDep):
    return {
        "error": None, 
        "result": await BookingService(db).get_all()
    }


@router.get("/me")
async def get_authorithed_items(
    db: DBDep, 
    user_id: userIdDep
):
    return {
        "error": None, 
        "result": await BookingService(db).get_me(user_id)
    }
