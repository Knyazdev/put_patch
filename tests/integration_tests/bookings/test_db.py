from src.schemas.booking import BookingAdd, Booking
from datetime import date


async def test_booking_crud(db):
    # (C)
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all(2))[0].id
    data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=10, day=2),
        date_to=date(year=2025, month=10, day=22),
        price=2000
    )
    new_price = 3000
    booking = await db.booking.add(data)
    assert booking
    id = booking.id

    # (R)
    item = await db.booking.get_one_or_none(id=id)
    assert item
    # (U)
    await db.booking.edit(Booking(**item.model_dump(exclude={"price"}), price=new_price), id=id)
    item = await db.booking.get_one_or_none(id=id)
    assert int(item.price) == new_price
    # (D)
    await db.booking.delete(id=id)

    await db.rollback()
    print(f"{booking=}")
