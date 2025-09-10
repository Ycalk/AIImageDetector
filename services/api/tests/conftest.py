import pytest
import pytest_asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import app as dirty_app
from api.utils import Config
from asgi_lifespan import LifespanManager
from faststream.rabbit import RabbitBroker
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator


@asynccontextmanager
async def fake_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    broker = RabbitBroker()
    app.state.detector_publisher = broker.publisher(detector_queue, detector_exchange)
    app.state.broker = broker
    yield


@pytest_asyncio.fixture(scope="function")
async def app(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[FastAPI, None]:
    monkeypatch.setattr(Config, "RABBIT_PASSWORD", "password")
    monkeypatch.setattr(Config, "DETECT_IMAGE_TIMEOUT", 1)
    monkeypatch.setattr(dirty_app.router, "lifespan_context", fake_lifespan)
    async with LifespanManager(dirty_app):
        yield dirty_app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def broker(app: FastAPI) -> RabbitBroker:
    return app.state.broker  # type: ignore
