from sqlalchemy.orm import Session
from app.models.database import Log
from app.core.config import settings
import os

class LogStorageService:
    def __init__(self, db: Session):
        self.db = db
        os.makedirs(settings.LOG_STORAGE_PATH, exist_ok=True)

    def store_log(self, session_id: str, source: str, file_path: str, parsed_data: dict):
        log = Log(
            session_id=session_id,
            source=source,
            file_path=file_path,
            timestamp=parsed_data.get("timestamp"),
            level=parsed_data.get("level"),
            module=parsed_data.get("module"),
            message=parsed_data.get("message"),
            raw_content=parsed_data.get("raw")
        )
        self.db.add(log)
        self.db.commit()
        return log
