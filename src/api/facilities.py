from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityRequest


router = APIRouter(prefix='/facility', tags=['Facilities'])


@router.get('')
async def items(db: DBDep):
    return {
        'error': None,
        'result': await db.facilities.get_all()
    }


@router.post('')
async def add(db: DBDep, request: FacilityRequest):
    item = await db.facilities.add(request)
    await db.commit()
    return {
        'error': None,
        'result': item
    }
