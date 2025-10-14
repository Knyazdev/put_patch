from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from sqlalchemy import select
from pydantic import EmailStr
from src.repositories.mappers.mappers import UserDataMapper, UserDataWithHashMapper
from sqlalchemy.exc import NoResultFound
from src.exceptions import (
    RecordNotFoundException
)



class UserRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound as ex:
            raise RecordNotFoundException from ex

        return UserDataWithHashMapper.map_to_domain_entity(model)
