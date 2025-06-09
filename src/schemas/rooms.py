from pydantic import BaseModel, Field
from typing import Optional


class RoomAdd(BaseModel):
    hotel_id: Optional[int] = 0
    title: str
    description: str
    price: int
    quantity: int = 0


class Room(RoomAdd):
    id: int


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
