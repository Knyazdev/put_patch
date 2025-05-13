from fastapi import FastAPI, Query, Body
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Tashkent', 'name': 'sochi'},
    {'id': 2, 'title': 'Nukus', 'name': 'moscow'}
]


class PartUpdate(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None


@app.get("/hotels")
def get_hotels(
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
    return {'error': None, 'result': hotels_result}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'error': None, 'result': {}}


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    global hotels
    id = hotels[-1]['id'] + 1
    hotels.append({'id': id, 'title': title, 'name': name})
    return {'error': None, 'result': {'id': id}}


@app.put("/hotel/{hotel_id}")
def update_hotel(hotel_id: int, title: str, name: str):
    global hotels
    result = None
    for index, hotel in enumerate(hotels):
        if hotel['id'] == hotel_id:
            hotels[index]['title'] = title
            hotels[index]['name'] = name
            result = hotels[index]
            break

    if not result:
        return {'error': {'code': 404, 'message': 'Object not found'}, 'result': None}
    return {'error': None, 'result': result}


@app.patch('/hotel/{hotel_id}')
def part_update_hotel(
    hotel_id: int,
    hotel_data: PartUpdate = None
):
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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
