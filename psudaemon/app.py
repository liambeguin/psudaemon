from fastapi import FastAPI
import uvicorn


def main():
    app = FastAPI()
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="info")
