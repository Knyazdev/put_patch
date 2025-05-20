from fastapi import Query, APIRouter, Body, Depends
from schemas.hotels import Hotel, HotelPatch
from .dependencies import PaginationParams
from typing import Annotated
from sqlalchemy import insert, select, func
from database import async_session_maker
from repositories.hotels import HotelRepository

router = APIRouter(prefix='/hotels', tags=['Hotels'])

hotels = [
    {'id': 1, 'title': 'Tashkent', 'name': 'uzbekistan'},
    {'id': 2, 'title': 'Nukus', 'name': 'uzbekistan'},
    {'id': 3, 'title': 'Dushanbe', 'name': 'tadjikistan'},
    {'id': 4, 'title': 'Ashqabat', 'name': 'turkmenistan'},
    {'id': 5, 'title': 'Bishkek', 'name': 'kirgiziya'},
    {'id': 6, 'title': 'Astana', 'name': 'kazakhstan'},
    {'id': 7, 'title': 'Moscow', 'name': 'russia'}
]


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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'error': None, 'result': {}}


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        query = await HotelRepository(session).add(**hotel_data.model_dump())
        await session.commit()
        id = await HotelRepository(session).get_insert_id(query)
        item = await HotelRepository(session).get_one_or_none(id=id)

    return {'status': 'OK', 'data': item}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    result = None
    for index, hotel in enumerate(hotels):
        if hotel['id'] == hotel_id:
            hotels[index]['title'] = hotel_data.title
            hotels[index]['name'] = hotel_data.name
            result = hotels[index]
            break

    if not result:
        return {'error': {'code': 404, 'message': 'Object not found'}, 'result': None}
    return {'error': None, 'result': result}


@router.patch('/{hotel_id}',
              summary="Partially update of hotels",
              description="About this patch"
              )
def part_update_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    result = None
    for index, hotel in enumerate(hotels):
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotels[index]['title'] = hotel_data.title
            if hotel_data.name:
                hotels[index]['name'] = hotel_data.name

            result = hotels[index]
            break
    if not result:
        return {'error': {'code': 404, 'message': 'Object not found'}, 'result': None}
    return {'error': None, 'result': result}
