from fastapi import APIRouter, HTTPException, Response, Request
from schemas.users import UserRequestAdd, UserAdd
from repositories.users import UserRepository
from database import async_session_maker
from services.auth import AuthService
from api.dependencies import userIdDep


router = APIRouter(prefix='/auth', tags=["Authentification"])


@router.post('/register')
async def register(data: UserRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    data_user = UserAdd(
        email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UserRepository(session).add(data_user)
        await session.commit()
    return {'status': 'OK'}


@router.post('/login')
async def login(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail='This email already exists')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401, detail='Wrong password')
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}


@router.get('/me')
async def get_me(user_id: userIdDep):
    async with async_session_maker() as session:
        return await UserRepository(session).get_one_or_none(id=user_id)


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'status': 'OK'}
