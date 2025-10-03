from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityRequest
from src.tasks.tasks import test_task
from fastapi_cache.decorator import cache


router = APIRouter(prefix='/facility', tags=['Facilities'])


@router.get('')
@cache(expire=10)
async def items(db: DBDep):
    return {
        'error': None,
        'result': await db.facilities.get_all()
    }


@router.post('')
async def add(db: DBDep, request: FacilityRequest):
    item = await db.facilities.add(request)
    await db.commit()

    test_task.delay()

    return {
        'error': None,
        'result': item
    }
