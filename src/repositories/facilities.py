from src.repositories.base import BaseRepository
from src.models.facilites import FacilityOrm
from src.schemas.facilities import Facility


class FacilityRepository(BaseRepository):
    model = FacilityOrm
    scheme = Facility
