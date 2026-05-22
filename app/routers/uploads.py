import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.core.dependencies import get_current_user
from app.utils.validators import ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_MB

UPLOAD_DIR = Path("uploads")
router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])


@router.post("/evidence")
async def upload_evidence(
    file: UploadFile = File(...),
    _=Depends(get_current_user),
):
    """
    Upload a photo of the resource condition for a return.
    Returns the stored path to use in POST /api/v1/returns/ as 'evidencia'.
    Accepted: jpg, jpeg, png, webp — max 5 MB.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Invalid file type '{file.content_type}'. Accepted: {ALLOWED_MIME_TYPES}",
        )

    content = await file.read()
    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"File too large. Maximum size is {MAX_UPLOAD_SIZE_MB} MB.",
        )

    suffix = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{suffix}"
    filepath = UPLOAD_DIR / filename
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(content)

    return {"path": f"uploads/{filename}", "filename": filename}
