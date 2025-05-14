from fastapi import Query, APIRouter, Body, Depends
from schemas.hotels import Hotel, HotelPatch
from dependencies import PaginationParams
from typing import Annotated

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
def get_hotels(
    pagination: Annotated[PaginationParams, Depends()],
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Названия")
):
    hotels_result = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_result.append(hotel)
    start = pagination.per_page * (pagination.page - 1)
    return {
        'error': None,
        'result': hotels_result[start:][:pagination.per_page]
    }


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'error': None, 'result': {}}


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Sochi",
        'value': {
            'title': "Sochi 5 star hotel",
            'name': 'sochi_u_berega'
        }
    },
    "2": {
        "summary": "Moscow",
        'value': {
            'title': "Moscow 5 star hotel",
            'name': 'moscow_hotel'
        }
    }
})):
    global hotels
    id = hotels[-1]['id'] + 1
    hotels.append({'id': id, 'title': hotel_data.title,
                  'name': hotel_data.name})
    return {'error': None, 'result': {'id': id}}


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
