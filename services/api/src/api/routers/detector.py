import base64
from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from messaging_schema.models.detect import (
    DetectionError,
    DetectionRequest,
    DetectionResponse,
)
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from api.utils import Config
from pydantic import ValidationError


router = APIRouter(prefix="/api", tags=["detector"])


@router.post(
    "/detect",
    response_model=DetectionResponse,
    responses={
        422: {"description": "Incorrect request format"},
        400: {"description": "Bad request"},
        504: {"description": "Request timed out"},
        500: {"description": "Internal server error"},
    },
)
async def detect(request: Request, image: UploadFile = File(...)):
    """Detect image generate by AI"""
    try:
        publisher: AsyncAPIPublisher = request.app.state.detector_publisher
        encoded_image = base64.b64encode(await image.read()).decode("utf-8")
        response = await publisher.request(
            DetectionRequest(
                image=encoded_image,
            ),
            timeout=Config.DETECT_IMAGE_TIMEOUT,
        )
        result = DetectionResponse.model_validate_json(response.body)
        if result.result > 1.0 or result.result < 0.0:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": (
                        "Invalid response from detection service. "
                        f"Expected result between 0.0 and 1.0, but got {result.result}"
                    )
                },
            )
        return result
    except ValidationError as e:
        try:
            error = DetectionError.model_validate_json(response.body)  # type: ignore
            raise HTTPException(status_code=422, detail=error.details)
        except ValidationError:
            raise HTTPException(status_code=500, detail={"message": str(e)})
    except TimeoutError:
        raise HTTPException(status_code=504, detail={"message": "Request timed out"})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})
