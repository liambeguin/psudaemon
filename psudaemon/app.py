from fastapi import FastAPI
import uvicorn

from .routers import monitoring


def main():
    app = FastAPI()
    app.include_router(monitoring.router)

    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="info")
