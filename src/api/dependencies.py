from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated
from services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Page", gt=0)]
    per_page: Annotated[int | None, Query(
        None, description="Page", gt=1, lt=30)]


def get_token(requset: Request) -> str:
    access_token = requset.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail="No auth code")
    return access_token


def get_current_user(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data['user_id']


userIdDep = Annotated[int, Depends(get_current_user)]
