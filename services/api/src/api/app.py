from fastapi import FastAPI
from .utils import Config


app = FastAPI(title=Config.API_NAME)
