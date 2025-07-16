from fastapi import APIRouter, File, UploadFile, HTTPException
from messaging_schema.exchanges import detector_exchange
from messaging_schema.queues import detector_queue
from messaging_schema.models.detect import DetectionError, DetectionRequest, DetectionResponse
from ..utils import broker, Config
import base64
from pydantic import ValidationError


router = APIRouter(prefix="/detector", tags=["detector"])


@router.post(
    "/detect",
    response_model=DetectionResponse,
    responses={
        422: {"description": "Incorrect request format"},
        400: {"description": "Validation error"},
        504: {"description": "Request timed out"},
        500: {"description": "Internal server error"},
    },
)
async def detect(image: UploadFile = File(...)):
    """Detect image generate by AI"""
    try:
        file_bytes = image.file.read()
        encoded_image = base64.b64encode(file_bytes).decode("utf-8")
        response = await broker.request(
            DetectionRequest(
                image=encoded_image,
            ),
            exchange=detector_exchange,
            queue=detector_queue,
            timeout=Config.DETECT_IMAGE_TIMEOUT,
        )
        return DetectionResponse.model_validate_json(response.body)
    except ValidationError as e:
        try:
            error = DetectionError.model_validate_json(response.body)
            raise HTTPException(status_code=422, detail=error.details)
        except ValidationError:
            raise HTTPException(status_code=500, detail={"message": str(e)})
    except TimeoutError:
        raise HTTPException(status_code=504, detail={"message": "Request timed out"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})
