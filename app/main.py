from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.api import router as api_router
import logging
import os

# Init FastAPI
app = FastAPI(title="Audio Processing API", version="1.0.0")

# Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app/logs/app.log"),
        logging.StreamHandler()
    ]
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Prepare dirs
app.mount("/output", StaticFiles(directory="data/output"), name="output")

# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)