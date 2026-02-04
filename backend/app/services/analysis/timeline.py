from sqlalchemy.orm import Session
from app.models.database import Log
from typing import List, Dict
from datetime import datetime, timedelta

class TimelineCorrelationService:
    def __init__(self, db: Session):
        self.db = db

    def build_timeline(self, session_id: str, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
        query = self.db.query(Log).filter(Log.session_id == session_id)

        if start_time:
            query = query.filter(Log.timestamp >= start_time)
        if end_time:
            query = query.filter(Log.timestamp <= end_time)

        logs = query.order_by(Log.timestamp).all()

        timeline = []
        for log in logs:
            timeline.append({
                'timestamp': log.timestamp,
                'module': log.module,
                'level': log.level,
                'message': log.message,
                'id': log.id
            })

        return timeline

    def find_related_events(self, session_id: str, reference_time: datetime, window_minutes: int = 5) -> List[Dict]:
        start = reference_time - timedelta(minutes=window_minutes)
        end = reference_time + timedelta(minutes=window_minutes)
        return self.build_timeline(session_id, start, end)
