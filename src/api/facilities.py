from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityRequest
from src.init import redis_manager
import json
from fastapi_cache.decorator import cache


router = APIRouter(prefix='/facility', tags=['Facilities'])


@router.get('')
@cache(expire=10)
async def items(db: DBDep):
    key = 'facilities'
    cache = await redis_manager.get(key)
    if cache:
        print('From cache')
        items = json.loads(cache)
    else:
        items = await db.facilities.get_all()
        await redis_manager.set(key, json.dumps(
            [item.model_dump() for item in items]), 60)

    return {
        'error': None,
        'result': items
    }


@router.post('')
async def add(db: DBDep, request: FacilityRequest):
    item = await db.facilities.add(request)
    await db.commit()
    return {
        'error': None,
        'result': item
    }
