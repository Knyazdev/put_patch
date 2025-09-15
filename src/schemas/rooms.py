from pydantic import BaseModel, Field, ConfigDict


class CoreRoom(BaseModel):
    title: str
    description: str
    price: int
    quantity: int = 0


class RoomRequest(CoreRoom):
    facility_ids: list[int] | None = None


class RoomAdd(CoreRoom):
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
