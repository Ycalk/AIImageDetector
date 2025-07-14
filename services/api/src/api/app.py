from fastapi import FastAPI
from logging import getLogger
from .utils import Config, broker
from .routers import detector
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    logger = getLogger("uvicorn")
    logger.info("Starting broker...")
    await broker.start()
    await broker.declare_exchange(detector_exchange)
    await broker.declare_queue(detector_queue)
    logger.info("Broker started successfully.")
    yield
    logger.info("Stopping broker...")
    await broker.stop()


app = FastAPI(title=Config.API_NAME, lifespan=lifespan)
app.include_router(detector.router)
