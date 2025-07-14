import uvicorn
from .utils import Config


def run():
    uvicorn.run("api:app", host="0.0.0.0", port=Config.SERVER_PORT)
