from sqlalchemy.orm import Session
from app.models.database import Log
from datetime import timedelta
from typing import List
import re

class LogCorrelationService:
    def __init__(self, db: Session):
        self.db = db

    def correlate_by_timestamp(self, session_id: str, timestamp, window_seconds: int = 5) -> List[Log]:
        start_time = timestamp - timedelta(seconds=window_seconds)
        end_time = timestamp + timedelta(seconds=window_seconds)

        return self.db.query(Log).filter(
            Log.session_id == session_id,
            Log.timestamp >= start_time,
            Log.timestamp <= end_time
        ).order_by(Log.timestamp).all()

    def correlate_by_request_id(self, session_id: str, request_id: str) -> List[Log]:
        logs = self.db.query(Log).filter(Log.session_id == session_id).all()

        matching_logs = []
        for log in logs:
            if log.raw_content and request_id in log.raw_content:
                matching_logs.append(log)

        return sorted(matching_logs, key=lambda x: x.timestamp or x.created_at)
