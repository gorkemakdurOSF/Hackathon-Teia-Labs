from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    API_KEY: str
    API_SECRET_KEY: str
    SHOP_URL: str
    API_VERSION: str
    REDIRECT_URI: str
    SCOPES: List[str]
    HOST: str
    PORT: int
    RELOAD: bool
    DB_CONNECTION_URI: str

    class Config:
        env_file = ".env"


SETTINGS = Settings()
