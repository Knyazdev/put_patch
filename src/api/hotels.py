from fastapi import Query, APIRouter, Body, Depends
from schemas.hotels import HotelAdd, HotelPatch
from .dependencies import PaginationParams, DBDep
from typing import Annotated

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get("")
async def get_hotels(
    pagination: Annotated[PaginationParams, Depends()],
    db: DBDep,
    title: str | None = Query(None, description="Названия"),
    location: str | None = Query(None, description="Location")
):
    per_page = pagination.per_page or 5
    return {
        'error': None,
        'result': await db.hotels.get_all(
            location=location,
            title=title,
            page=pagination.page,
            offset=per_page
        )
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Sochi",
        'value': {
            'title': "Sochi 5 star hotel",
            'location': 'sochi_u_berega'
        }
    },
    "2": {
        "summary": "Moscow",
        'value': {
            'title': "Moscow 5 star hotel",
            'location': 'moscow_hotel'
        }
    }
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {'status': 'OK', 'data': hotel}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
              summary="Partially update of hotels",
              description="About this patch"
              )
async def part_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {'status': 'OK'}


@router.get('/{hotel_id}')
async def get_one_item(db: DBDep, hotel_id: int):
    result = await db.hotels.get_one_or_none(id=hotel_id)
    return {'status': 'OK', 'hotel': result}
