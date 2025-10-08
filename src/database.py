from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

engine = create_async_engine(settings.DB_URL, echo=True)
engine_null_pull = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pull = async_sessionmaker(
    bind=engine_null_pull, expire_on_commit=False
)

session = async_session_maker()


class Base(DeclarativeBase):
    pass
