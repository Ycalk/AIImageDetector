import uvicorn
from .utils import Config
from dotenv import load_dotenv


def run():
    load_dotenv()
    uvicorn.run("api:app", host="0.0.0.0", port=Config.SERVER_PORT)
