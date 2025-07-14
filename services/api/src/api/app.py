from fastapi import FastAPI
from .utils import Config
from .routers import detector


app = FastAPI(title=Config.API_NAME)
app.include_router(detector.router)
