from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from .models import init_database, Database
from .routes import clothes, wardrobe, outfit
from .settings import SETTINGS


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(clothes.router)
    app.include_router(wardrobe.router)
    app.include_router(outfit.router)

    app.mount('/', StaticFiles(directory='/opt/ssd/osf-hackathon-2022/images/'), name='static')

    database = Database

    @app.on_event('startup')
    async def startup():
        nonlocal database
        database = init_database(SETTINGS.DB_CONNECTION_URI)
        await database.database.clothes.delete_many({})
        await database.database.outfit.delete_many({})
        await database.database.wardrobe.delete_many({})
        await database.database.user.delete_many({})

    return app
