import asyncio
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Database(metaclass=Singleton):
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


database = Database()


def init_database(
        uri: Optional[str],
        username: Optional[str] = None,
        password: Optional[str] = None
) -> Database:
    schema = uri.split("/")[-1]
    schema = schema.split("?")[0]
    if username is None and password is None:
        database.client = AsyncIOMotorClient(uri)
    else:
        database.client = AsyncIOMotorClient(uri, username=username, password=password)
    database.database = database.client[schema]
    asyncio.ensure_future(database.database["file"].create_index("path_hash", unique=True))

    return database
