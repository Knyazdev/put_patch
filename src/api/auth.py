from fastapi import APIRouter, HTTPException, Response
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import userIdDep, DBDep
from src.exceptions import (
    UserAlreadyExistException,
    HttpUserAlreadyExistException,
    UserNotExistException,
    WrongUserPasswordException
)


router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register")
async def register(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register(data)
    except UserAlreadyExistException as ex:
        raise HttpUserAlreadyExistException from ex
    return {
        "status": "OK"
    }


@router.post("/login")
async def login(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login(data)
        response.set_cookie("access_token", access_token)
        return {
            "access_token": access_token
        }
    except UserNotExistException as ex:
        raise HTTPException(status_code=401, detail=ex.detail)
    except WrongUserPasswordException as ex:
        raise HTTPException(status_code=401, detail=ex.detail)


@router.get("/me")
async def get_me(user_id: userIdDep, db: DBDep):
    return await AuthService(db).get_me(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "status": "OK"
    }
