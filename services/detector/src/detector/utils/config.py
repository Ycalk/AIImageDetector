import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "model.pt")

    RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_USER = os.getenv("RABBIT_USER", "detector")
    RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "")

    if not RABBIT_PASSWORD:
        raise ValueError("RABBIT_PASSWORD must be set in the environment variables")
