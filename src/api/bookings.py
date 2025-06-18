from fastapi import APIRouter, Body
from schemas.booking import BookingRequest, BookingAdd
from .dependencies import DBDep, userIdDep


router = APIRouter(prefix='/bookings', tags=['Booking'])


@router.post("/")
async def create_booking(
    db: DBDep,
    user_id: userIdDep,
    req: BookingRequest = Body()
):
    room = await db.rooms.get_one_or_none(id=req.room_id)
    data = BookingAdd(user_id=user_id, price=room.price, **req.model_dump())
    booking = await db.booking.add(data)
    await db.commit()

    return {'status': 'OK', 'data': booking}
