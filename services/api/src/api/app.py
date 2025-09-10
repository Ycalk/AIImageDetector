from fastapi import FastAPI
from logging import getLogger
from .utils import Config
from faststream.rabbit import RabbitBroker
from faststream.security import SASLPlaintext
from .routers import detector
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from importlib.metadata import version


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    logger = getLogger("uvicorn")
    logger.info("Starting broker...")
    broker = RabbitBroker(
        host=Config.RABBIT_HOST,
        port=Config.RABBIT_PORT,
        security=SASLPlaintext(
            username=Config.RABBIT_USER,
            password=Config.RABBIT_PASSWORD,
        ),
    )
    detector_publisher = broker.publisher(
        detector_queue,
        detector_exchange,
        title="Detector Publisher",
        description="Publisher for sending detection requests",
    )
    await broker.start()
    app.state.detector_publisher = detector_publisher
    logger.info("Broker started successfully.")

    yield

    logger.info("Stopping broker...")
    await broker.stop()


app = FastAPI(
    title=Config.API_NAME,
    lifespan=lifespan,
    version=version("api"),
    docs_url=Config.DOCS_PREFIX + "/docs",
    redoc_url=Config.DOCS_PREFIX + "/redoc",
)

app.include_router(detector.router)
