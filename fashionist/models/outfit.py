from typing import List, Optional

from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base
from .clothes import Clothes


class Outfit(BaseModel, Base):
    __collection__ = "outfit"

    id: PyObjectId = Field()
    clothes: List[Clothes] = Field()
    tags: List[str] = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UpdateOutfit(BaseModel):
    clothes: Optional[List[Clothes]]
    tags: Optional[List[str]]
