from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import clothes
from .routes import wardrobe


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

    return app
