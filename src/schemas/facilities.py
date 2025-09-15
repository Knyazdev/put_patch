from pydantic import BaseModel


class FacilityRequest(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str


class RoomFacilityRequest(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityRequest):
    id: int
