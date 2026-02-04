from sqlalchemy.orm import Session
from app.models.database import Log
from typing import List

class ErrorLogDetector:
    def __init__(self, db: Session):
        self.db = db
        self.error_levels = ['ERROR', 'EXCEPTION', 'FATAL']

    def detect_errors(self, session_id: str) -> List[Log]:
        return self.db.query(Log).filter(
            Log.session_id == session_id,
            Log.level.in_(self.error_levels)
        ).order_by(Log.timestamp).all()

    def detect_errors_by_pattern(self, session_id: str, pattern: str) -> List[Log]:
        logs = self.db.query(Log).filter(Log.session_id == session_id).all()
        return [log for log in logs if pattern.lower() in (log.message or '').lower()]
