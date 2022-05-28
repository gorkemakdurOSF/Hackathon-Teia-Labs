from typing import List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base


class Clothes(BaseModel, Base):
    __collection__ = "clothes"

    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    url: str = Field()
    tags: List[str] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UpdateClothes(BaseModel):
    tags: List[str]
