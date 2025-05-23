from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()


class Base(DeclarativeBase):
    pass
