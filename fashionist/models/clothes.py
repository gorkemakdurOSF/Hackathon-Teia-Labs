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
    value: bytes = Field()
    isLiked: bool = Field(default_factory=lambda: random.randint(0, 10) > 3)
    tags: List[str] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, bytes: str}


class UpdateClothes(BaseModel):
    tags: List[str]


class CLothesOut(BaseModel):
    id: PyObjectId
    url: str 
    value: str
    isLiked: bool
    tags: List[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}