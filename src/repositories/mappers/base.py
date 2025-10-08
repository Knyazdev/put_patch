from typing import TypeVar
from pydantic import BaseModel
from src.database import Base

SchemeType = TypeVar("SchemeType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper:
    db_model: type[DBModelType] = None
    scheme: type[SchemeType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.scheme.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
