from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityRequest
from fastapi_cache.decorator import cache
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facility", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def items(db: DBDep):
    return {
        "error": None, 
        "result": await FacilityService(db).items()
    }


@router.post("")
async def add(db: DBDep, request: FacilityRequest):
    return {
        "error": None, 
        "result": await FacilityService(db).add(request)
    }
