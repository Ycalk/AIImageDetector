import pytest
import asyncio
import base64
import os
from api.utils import Config
from httpx import AsyncClient
from faststream.rabbit import RabbitBroker, RabbitMessage
from messaging_schema.models.detect import (
    DetectionResponse,
    DetectionRequest,
    DetectionError,
)
from io import BytesIO
from faststream.rabbit import TestRabbitBroker
from pydantic import ValidationError
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "detection_result",
    [0.0, 0.5, 1.0, -0.1, 1.1],
)
async def test_different_results_from_model(
    broker: RabbitBroker, client: AsyncClient, detection_result: float
) -> None:
    image_bytes = os.urandom(16)
    message_event = asyncio.Event()

    async def subscriber_handler(message: RabbitMessage) -> DetectionResponse:
        message_event.set()
        try:
            request = DetectionRequest.model_validate_json(message.body)
            assert base64.b64decode(request.image) == image_bytes
        except ValidationError:
            pytest.fail(f"Incorrect request: {message.body}")
        return DetectionResponse(result=detection_result)

    broker.subscriber(detector_queue, detector_exchange)(subscriber_handler)

    async with TestRabbitBroker(broker=broker):
        response = await client.post(
            "/api/detect", files={"image": ("test.png", image_bytes)}
        )
        try:
            await asyncio.wait_for(message_event.wait(), timeout=1.0)
        except asyncio.TimeoutError:
            pytest.fail("Subscriber was not called")

    # If the detection result is out of bounds, we expect a 500 error
    if detection_result < 0.0 or detection_result > 1.0:
        assert response.status_code == 500
        return

    assert response.status_code == 200
    try:
        response_model = DetectionResponse.model_validate(response.json())
    except ValidationError:
        pytest.fail(f"Incorrect response: {response.json()}")
    assert response_model.result == detection_result


@pytest.mark.asyncio
async def test_model_not_available(broker: RabbitBroker, client: AsyncClient) -> None:
    image_bytes = os.urandom(16)

    async with TestRabbitBroker(broker=broker):
        post_func = client.post(
            "/api/detect", files={"image": ("test.png", image_bytes)}
        )
        try:
            response = await asyncio.wait_for(
                post_func, timeout=Config.DETECT_IMAGE_TIMEOUT + 1
            )
        except asyncio.TimeoutError:
            pytest.fail("Subscriber was not called")

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_invalid_request_format(broker: RabbitBroker, client: AsyncClient):
    image_bytes = os.urandom(16)
    message_event = asyncio.Event()

    async def subscriber_handler(message: RabbitMessage):
        message_event.set()
        return DetectionError(
            error="Incorrect image format", details="Invalid image format"
        )

    broker.subscriber(detector_queue, detector_exchange)(subscriber_handler)

    async with TestRabbitBroker(broker=broker):
        response = await client.post(
            "/api/detect", files={"image": ("test.png", image_bytes)}
        )
        await asyncio.wait_for(message_event.wait(), timeout=1.0)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_timeout_error(broker: RabbitBroker, client: AsyncClient):
    image_bytes = os.urandom(16)

    async def subscriber_handler(_: RabbitMessage):
        await asyncio.sleep(Config.DETECT_IMAGE_TIMEOUT + 1)

    broker.subscriber(detector_queue, detector_exchange)(subscriber_handler)

    async with TestRabbitBroker(broker=broker):
        response = await client.post(
            "/api/detect", files={"image": ("test.png", image_bytes)}
        )

    assert response.status_code == 504


@pytest.mark.asyncio
async def test_empty_file(broker: RabbitBroker, client: AsyncClient):
    empty_file = BytesIO(b"")

    async def subscriber_handler(message: RabbitMessage):
        return DetectionResponse(result=0.5)

    broker.subscriber(detector_queue, detector_exchange)(subscriber_handler)

    async with TestRabbitBroker(broker=broker):
        response = await client.post(
            "/api/detect", files={"image": ("empty.png", empty_file)}
        )

    assert response.status_code == 200
    assert response.json()["result"] == 0.5
