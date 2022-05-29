from email.policy import default
from typing import List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base
import random


class Clothes(BaseModel, Base):
    __collection__ = "clothes"

    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    url: str = Field()
    isLiked: bool = Field(default_factory=lambda: random.randint(0, 10) > 3)
    tags: List[str] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateClothes(BaseModel):
    tags: List[str]
