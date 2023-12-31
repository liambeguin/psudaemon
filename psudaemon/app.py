import uvicorn

from fastapi import FastAPI

from .context import load_settings
from .routers import monitoring, units


def main():
    settings = load_settings()

    app = FastAPI()
    app.include_router(units.router)
    app.include_router(monitoring.router)

    uvicorn.run(app, host='0.0.0.0', **dict(settings.uvicorn))
