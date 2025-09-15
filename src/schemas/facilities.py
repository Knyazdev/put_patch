from pydantic import BaseModel


class FacilityRequest(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str
