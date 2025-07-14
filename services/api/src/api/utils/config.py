import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_NAME = "AI Image Detector"
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

    RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_USER = os.getenv("RABBIT_USER", "api")
    RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "")

    DETECT_IMAGE_TIMEOUT = int(os.getenv("DETECT_IMAGE_TIMEOUT", 20))

    if not RABBIT_PASSWORD:
        raise ValueError("RABBIT_PASSWORD must be set in the environment variables")
