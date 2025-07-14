from fastapi import APIRouter, File, UploadFile, HTTPException


router = APIRouter(prefix="/detector", tags=["detector"])


@router.get("/detect")
async def detect(image: UploadFile = File(...)):
    """Detect image generate by AI"""
    try:
        file_bytes = image.file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})
