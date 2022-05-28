from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base
from .clothes import Clothes


class Outfit(BaseModel, Base):
    __collection__ = "outfit"

    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    clothes: List[Clothes] = Field()
    tags: List[str] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UpdateOutfit(BaseModel):
    clothes: Optional[List[Clothes]]
    tags: Optional[List[str]]
