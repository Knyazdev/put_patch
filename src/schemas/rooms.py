from pydantic import BaseModel, Field, ConfigDict
from src.schemas.facilities import Facility


class CoreRoom(BaseModel):
    title: str
    description: str
    price: int
    quantity: int = 0


class RoomRequest(CoreRoom):
    facility_ids: list[int] = []


class RoomAdd(CoreRoom):
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatchRequest(RoomPatch):
    facility_ids: list[int] = []
