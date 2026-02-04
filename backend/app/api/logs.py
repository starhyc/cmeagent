from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_auth
from app.core.config import settings
from app.services.log_normalizer import LogNormalizer
from app.services.log_storage import LogStorageService
import os
import uuid
import aiofiles

router = APIRouter()

@router.post("/logs/upload")
async def upload_log(file: UploadFile = File(...), db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    os.makedirs(settings.LOG_STORAGE_PATH, exist_ok=True)

    session_id = str(uuid.uuid4())
    file_path = os.path.join(settings.LOG_STORAGE_PATH, f"{session_id}_{file.filename}")

    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)

    normalizer = LogNormalizer()
    storage = LogStorageService(db)

    with open(file_path, 'r') as f:
        for line in f:
            parsed = normalizer.normalize(line)
            if parsed:
                storage.store_log(session_id, file.filename, file_path, parsed)

    return {"session_id": session_id, "file_path": file_path, "filename": file.filename}
