from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_auth
from app.services.report.storage import ReportStorageService
from app.services.report.pandoc_converter import PandocConverter
from app.services.report.markdown_generator import MarkdownReportGenerator
from app.services.analysis.timeline import TimelineCorrelationService
from app.services.analysis.call_chain import CallChainAnalyzer
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

router = APIRouter()

class ReportGenerateRequest(BaseModel):
    session_id: str
    title: str
    analysis_result: dict

class ReportGenerateResponse(BaseModel):
    report_id: int
    title: str

class ReportHistoryItem(BaseModel):
    id: int
    title: str
    session_id: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/reports/generate", response_model=ReportGenerateResponse)
async def generate_report(request: ReportGenerateRequest, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    timeline_service = TimelineCorrelationService(db)
    timeline = timeline_service.build_timeline(request.session_id)

    call_chain_analyzer = CallChainAnalyzer(db)
    call_chain = call_chain_analyzer.analyze_call_chain(request.session_id, timeline[0]['timestamp'] if timeline else None)
    dependencies = call_chain_analyzer.extract_module_dependencies(call_chain)

    generator = MarkdownReportGenerator()
    markdown_content = generator.generate_report(request.title, request.analysis_result, timeline, call_chain, dependencies)

    storage = ReportStorageService(db)
    report = storage.save_report(request.session_id, request.title, markdown_content, user.get('user_id', 1))

    return ReportGenerateResponse(report_id=report.id, title=report.title)

@router.get("/reports/history", response_model=List[ReportHistoryItem])
async def get_report_history(db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    storage = ReportStorageService(db)
    reports = storage.list_reports()
    return reports

@router.get("/reports/{report_id}/export/markdown")
async def export_markdown(report_id: int, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    storage = ReportStorageService(db)
    report = storage.get_report(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(report.markdown_path, media_type="text/markdown", filename=f"{report.title}.md")

@router.get("/reports/{report_id}/export/pdf")
async def export_pdf(report_id: int, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    storage = ReportStorageService(db)
    report = storage.get_report(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if not report.pdf_path or not os.path.exists(report.pdf_path):
        converter = PandocConverter()
        pdf_path = report.markdown_path.replace('.md', '.pdf')
        converter.convert_to_pdf(report.markdown_path, pdf_path)
        report.pdf_path = pdf_path
        db.commit()

    return FileResponse(report.pdf_path, media_type="application/pdf", filename=f"{report.title}.pdf")
