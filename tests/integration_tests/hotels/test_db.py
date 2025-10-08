from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    data = HotelAdd(title="Hotel Grand Base London", location="London")

    new_hotel = await db.hotels.add(data)
    await db.commit()
    print(f"{new_hotel=}")
