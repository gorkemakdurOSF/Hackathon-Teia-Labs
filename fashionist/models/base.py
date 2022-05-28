from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar

from pydantic import BaseModel

from . import PyObjectId
from . import database


T = TypeVar("T", bound=BaseModel)


class Base:
    __collection__ = "base"

    @classmethod
    async def get_or_create(cls, filters: Dict[str, Any], data: T) -> T:
        return await database.database[cls.__collection__].find_one_and_update(
            filters,
            {"$setOnInsert": data.dict(by_alias=True)},
            upsert=True,
            return_document=False
        )

    @classmethod
    async def create_many(cls, data: List[T]) -> List[PyObjectId]:
        result = await database.database[cls.__collection__].insert_many(
            [obj.dict(by_alias=True) for obj in data]
        )

        return result.inserted_idsg

    @classmethod
    async def create(cls, data: T) -> PyObjectId:
        result = await database.database[cls.__collection__].insert_one(
            data.dict(by_alias=True)
        )
        return result.inserted_id

    @classmethod
    async def read(
            cls,
            order: Tuple[str, bool] = Ellipsis,
            offset: int = 0,
            limit: int = 100,
            **kwargs
    ) -> List[T]:
        cursor = database.database[cls.__collection__].find(kwargs)
        if order != Ellipsis:
            cursor = cursor.sort(order[0], 1 if order[1] else -1)

        return await cursor.skip(offset).to_list(limit + offset)

    @classmethod
    async def read_extra(cls, query, extra) -> List[T]:
        return await database.database[cls.__collection__].find(query, extra).to_list()

    @classmethod
    async def upsert(cls, data: T) -> int:
        return await database.database[cls.__collection__].update(
            {"_id": data.id},
            {"$set": data.dict(exclude_unset=True, by_alias=True)},
            {"upsert": True}
        )

    @classmethod
    async def update(cls, _id: PyObjectId, data: T) -> int:
        result = await database.database[cls.__collection__].update_one(
            {"_id": _id},
            {"$set": data.dict(exclude_unset=True, by_alias=True)}
        )

        return result.modified_count

    @classmethod
    async def delete(cls, _id: PyObjectId) -> int:
        result = await database.database[cls.__collection__].delete_one(
            {"_id": _id}
        )
        return result.deleted_count
