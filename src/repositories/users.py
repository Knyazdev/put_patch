from repositories.base import BaseRepository
from models.users import UsersOrm
from schemas.users import User


class UserRepository(BaseRepository):
    model = UsersOrm
    scheme = User
