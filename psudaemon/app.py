import uvicorn

from fastapi import FastAPI

from .context import load_settings
from .routers import monitoring, units, settings


def main():
    app = FastAPI()
    s = load_settings()

    app.include_router(settings.router)
    app.include_router(monitoring.router)
    app.include_router(units.router)

    uvicorn.run(app, host='0.0.0.0', **dict(s.uvicorn))
