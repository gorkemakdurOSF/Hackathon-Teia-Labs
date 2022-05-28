from pydantic import BaseModel, Field

from . import PyObjectId
from .base import Base


class User(BaseModel, Base):
    __collection__ = "clothes"

    id: PyObjectId = Field()
    unique_index: str = Field()
    wardrobe: PyObjectId = Field

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
