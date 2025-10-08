from fastapi import APIRouter, HTTPException, Response
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import userIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register")
async def register(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    data_user = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(data_user)
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="This email already exists")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: userIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
