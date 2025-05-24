from fastapi import APIRouter
from schemas.users import UserRequestAdd, UserAdd
from repositories.users import UserRepository
from database import async_session_maker

from passlib.context import CryptContext

router = APIRouter(prefix='/auth', tags=["Authentification"])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/register')
async def register(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    data_user = UserAdd(
        email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UserRepository(session).add(data_user)
        await session.commit()
    return {'status': 'OK'}
