from fastapi import Query, APIRouter, Body, Depends
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationParams, DBDep
from typing import Annotated
from datetime import date
from src.exceptions import (
    HotelNotFoundException,
    HttpHotelNotFoundException
)
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: Annotated[PaginationParams, Depends()],
    db: DBDep,
    title: str | None = Query(None, description="Названия"),
    location: str | None = Query(None, description="Location"),
    date_from: date = Query(example="2025-12-01"),
    date_to: date = Query(example="2025-07-01"),
):
    return {
        "error": None,
        "result": await HotelService(db).get_filtered_by_time(
            pagination,
            location,
            title,
            date_from,
            date_to
        )
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).delete(hotel_id)
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex
    return {"status": "OK"}


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Sochi 5 star hotel", "location": "sochi_u_berega"},
            },
            "2": {
                "summary": "Moscow",
                "value": {"title": "Moscow 5 star hotel", "location": "moscow_hotel"},
            },
        }
    ),
):
    hotel = await HotelService(db).add(hotel_data)

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    try:
        await HotelService(db).edit(hotel_id=hotel_id, hotel_data=hotel_data)
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}", summary="Partially update of hotels", description="About this patch"
)
async def part_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    try:
        await HotelService(db).edit(hotel_id=hotel_id, hotel_data=hotel_data, exclude=True)
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex
    return {"status": "OK"}


@router.get("/{hotel_id}")
async def get_one_item(db: DBDep, hotel_id: int):
    try:
        return {
            "status": "OK", 
            "hotel": await HotelService(db).get_one(hotel_id)
            }
    except HotelNotFoundException as ex:
        raise HttpHotelNotFoundException from ex
