import io
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue
from messaging_schema.models.detect import (
    DetectionError,
    DetectionRequest,
    DetectionResponse,
)
from ..utils import broker, Model
from faststream import Context
from PIL import Image
from PIL import UnidentifiedImageError


@broker.subscriber(detector_queue, detector_exchange)
async def detect(
    request: DetectionRequest, model: Model = Context()
) -> DetectionResponse | DetectionError:
    try:
        image = Image.open(io.BytesIO(request.image)).convert("RGB")
        return DetectionResponse(result=model(image))
    except UnidentifiedImageError:
        return DetectionError(
            error="Invalid image format",
            details="The provided image could not be identified or is not a valid image format.",
        )
    except Exception as e:
        return DetectionError(
            error="Image processing error",
            details=str(e),
        )
