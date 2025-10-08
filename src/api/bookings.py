from fastapi import APIRouter, Body, HTTPException
from src.schemas.booking import BookingRequest, BookingAdd
from .dependencies import DBDep, userIdDep
from src.exceptions import RecordNotFoundException


router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.post("")
async def create_booking(db: DBDep, user_id: userIdDep, req: BookingRequest = Body()):
    try:
        room = await db.rooms.get_one(id=req.room_id)
    except RecordNotFoundException as ex:
        raise HTTPException(404, detail=ex.detail)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    data = BookingAdd(user_id=user_id, price=room.price, **req.model_dump())
    # booking = await db.booking.add(data)
    booking = await db.booking.add_booking(data, hotel_id=hotel.id)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("/")
async def get_all(db: DBDep):
    return {"error": None, "result": await db.booking.get_all()}


@router.get("/me")
async def get_authorithed_items(db: DBDep, user_id: userIdDep):
    return {"error": None, "result": await db.booking.get_mine(user_id)}
