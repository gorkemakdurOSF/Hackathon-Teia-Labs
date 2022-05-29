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
    def startup():
        nonlocal database
        database = init_database(SETTINGS.DB_CONNECTION_URI)

    return app
