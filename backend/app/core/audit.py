from fastapi import Request
from sqlalchemy.orm import Session
from app.models.database import AuditLog
from app.core.database import SessionLocal
from datetime import datetime
import json

async def audit_log_middleware(request: Request, call_next):
    response = await call_next(request)

    if hasattr(request.state, "user"):
        db = SessionLocal()
        try:
            audit = AuditLog(
                user_id=request.state.user.get("user_id"),
                action=f"{request.method} {request.url.path}",
                resource=request.url.path,
                details=json.dumps({"status_code": response.status_code})
            )
            db.add(audit)
            db.commit()
        finally:
            db.close()

    return response
