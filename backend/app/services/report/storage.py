from sqlalchemy.orm import Session
from app.models.database import Report
from app.core.config import settings
import os

class ReportStorageService:
    def __init__(self, db: Session):
        self.db = db
        os.makedirs(settings.REPORT_STORAGE_PATH, exist_ok=True)

    def save_report(self, session_id: str, title: str, markdown_content: str, user_id: int) -> Report:
        markdown_path = os.path.join(settings.REPORT_STORAGE_PATH, f"{session_id}.md")

        with open(markdown_path, 'w') as f:
            f.write(markdown_content)

        report = Report(
            session_id=session_id,
            title=title,
            markdown_path=markdown_path,
            created_by=user_id
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_report(self, report_id: int) -> Report:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def list_reports(self, user_id: int = None):
        query = self.db.query(Report)
        if user_id:
            query = query.filter(Report.created_by == user_id)
        return query.order_by(Report.created_at.desc()).all()
