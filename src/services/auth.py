from datetime import datetime, timedelta, timezone
from src.config import settings
import jwt
from passlib.context import CryptContext
from src.services.base import BaseService
from src.schemas.users import UserRequestAdd, UserAdd
from src.exceptions import (
    RecordAlreadyExistException,
    UserAlreadyExistException,
    RecordNotFoundException,
    UserNotExistException,
    WrongUserPasswordException,
    IncorrectTokenException
)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError as ex:
            raise IncorrectTokenException from ex
        except jwt.exceptions.ExpiredSignatureError as ex:
            raise IncorrectTokenException from ex
        
    async def register(self, request: UserRequestAdd):
        hashed_password = self.pwd_context.hash(request.password)
        data_user = UserAdd(email=request.email, hashed_password=hashed_password)
        try:
            user = await self.db.users.add(data_user)
            await self.db.commit()
        except RecordAlreadyExistException as ex:
            raise UserAlreadyExistException from ex
        return user
    
    async def login(self, request: UserRequestAdd):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=request.email)
        except RecordNotFoundException as ex:
            raise UserNotExistException from ex
        
        if not self.verify_password(request.password, user.hashed_password):
            raise WrongUserPasswordException
        
        return self.create_access_token({"user_id": user.id})
    
    async def get_me(self, user_id:int):
        return await self.db.users.get_one_or_none(id=user_id)
        
