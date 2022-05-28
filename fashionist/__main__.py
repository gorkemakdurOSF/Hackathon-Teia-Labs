import uvicorn
from .settings import SETTINGS


def run():
    uvicorn.run(
        'fashionist:create_app',
        factory=True,
        host=SETTINGS.HOST,
        port=SETTINGS.PORT,
        reload=SETTINGS.RELOAD
    )


if __name__ == '__main__':
    run()
