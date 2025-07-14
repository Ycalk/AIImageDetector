import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_NAME = "AI Image Detector"
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
