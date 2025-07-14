from logging import Logger
from importlib.metadata import version
from faststream import FastStream, Context
from faststream import context
from .utils import broker, Model, Config

from .handlers.detect import detector_exchange, detector_queue

app = FastStream(
    broker,
    title="Detector Service",
    version=version("detector"),
    description="Service for detecting images using a pre-trained model.",
)


@app.on_startup
async def on_startup(logger: Logger = Context()):
    logger.info("Starting Detector app...")
    await broker.connect()
    await broker.declare_exchange(detector_exchange)
    await broker.declare_queue(detector_queue)

    context.set_global("model", Model(Config.MODEL_PATH))


@app.after_startup
async def after_startup(logger: Logger = Context()):
    logger.info(f"Detector Service version {app.version} started successfully.")


@app.on_shutdown
async def on_shutdown(
    logger: Logger = Context(),
):
    logger.info("Shutting down Detector Service ...")
    await broker.stop()
    logger.info("Detector Service shutdown complete.")
