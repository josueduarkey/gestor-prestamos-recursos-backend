import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.core.dependencies import get_current_user, require_roles
from app.utils.validators import ALLOWED_MIME_TYPES, MAX_UPLOAD_SIZE_MB

UPLOAD_DIR = Path("uploads")
router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])


async def _save_file(file: UploadFile, subfolder: str = "") -> dict:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Invalid file type '{file.content_type}'. Accepted: {ALLOWED_MIME_TYPES}",
        )
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"File too large. Maximum size is {MAX_UPLOAD_SIZE_MB} MB.",
        )
    suffix = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{suffix}"
    dest = UPLOAD_DIR / subfolder if subfolder else UPLOAD_DIR
    dest.mkdir(parents=True, exist_ok=True)
    (dest / filename).write_bytes(content)
    path = f"uploads/{subfolder}/{filename}" if subfolder else f"uploads/{filename}"
    return {"path": path, "filename": filename}


@router.post("/evidence")
async def upload_evidence(
    file: UploadFile = File(...),
    _=Depends(get_current_user),
):
    """
    Photo of resource condition for a return.
    Use the returned 'path' as 'evidencia' in POST /api/v1/returns/.
    """
    return await _save_file(file, subfolder="evidence")


@router.post("/resource-image")
async def upload_resource_image(
    file: UploadFile = File(...),
    _=Depends(require_roles("admin", "gestor")),
):
    """
    Photo for a resource/tool.
    Use the returned 'path' as 'imagen' in POST or PUT /api/v1/resources/.
    Accepted: jpg, jpeg, png, webp — max 5 MB.
    """
    return await _save_file(file, subfolder="resources")
