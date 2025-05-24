from fastapi import Query, APIRouter, Body, Depends
from schemas.hotels import HotelAdd, HotelPatch
from .dependencies import PaginationParams
from typing import Annotated
from database import async_session_maker
from repositories.hotels import HotelRepository

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get("")
async def get_hotels(
    pagination: Annotated[PaginationParams, Depends()],
    title: str | None = Query(None, description="Названия"),
    location: str | None = Query(None, description="Location")
):
    async with async_session_maker() as session:
        per_page = pagination.per_page or 5
        return {
            'error': None,
            'result': await HotelRepository(session).get_all(
                location=location,
                title=title,
                page=pagination.page,
                offset=per_page
            )
        }


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
              summary="Partially update of hotels",
              description="About this patch"
              )
async def part_update_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {'status': 'OK'}


@router.get('/{hotel_id}')
async def get_one_item(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelRepository(session).get_one_or_none(id=hotel_id)
        return {'status': 'OK', 'hotel': result}
