from typing import List, Optional

from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base


class Wardrobe(BaseModel, Base):
    __collection__ = "wardrobe"

    id: PyObjectId = Field()
    clothes: List[PyObjectId] = Field()
    outfit: List[PyObjectId] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UpdateWardrobe(BaseModel):
    clothes: Optional[List[PyObjectId]]
    outfit: Optional[List[PyObjectId]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
