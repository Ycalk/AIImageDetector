import os
from typing import Final


class Config:
    API_NAME: Final[str] = os.getenv("API_NAME", "AI Image Detector")
    DOCS_PREFIX: Final[str] = os.getenv("DOCS_PREFIX", "")
    SERVER_PORT: Final[int] = int(os.getenv("SERVER_PORT", 8000))

    RABBIT_PORT: Final[int] = int(os.getenv("RABBIT_PORT", 5672))
    RABBIT_HOST: Final[str] = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_USER: Final[str] = os.getenv("RABBIT_USER", "api")
    RABBIT_PASSWORD: Final[str] = os.getenv("RABBIT_PASSWORD", "")

    DETECT_IMAGE_TIMEOUT: Final[int] = int(os.getenv("DETECT_IMAGE_TIMEOUT", 20))

    if not RABBIT_PASSWORD:
        raise ValueError("RABBIT_PASSWORD must be set in the environment variables")
