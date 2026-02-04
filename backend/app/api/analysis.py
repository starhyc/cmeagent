from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_auth
from app.services.analysis.error_detector import ErrorLogDetector
from app.services.analysis.call_chain import CallChainAnalyzer
from app.services.analysis.root_cause import RootCauseAnalyzer
from app.services.analysis.issue_ranking import IssueRankingService
from app.services.analysis.performance import PerformanceAnomalyDetector
from app.services.analysis.aggregator import AnalysisResultAggregator
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()
analysis_cache: Dict[str, dict] = {}

class AnalysisRequest(BaseModel):
    session_id: str

class AnalysisResponse(BaseModel):
    task_id: str
    status: str

class AnalysisStatusResponse(BaseModel):
    status: str
    progress: int = 0

@router.post("/analysis/trigger", response_model=AnalysisResponse)
async def trigger_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user: dict = Depends(require_auth)):
    task_id = f"analysis_{request.session_id}"
    analysis_cache[task_id] = {"status": "running", "progress": 0}
    background_tasks.add_task(run_analysis, request.session_id, task_id, db)
    return AnalysisResponse(task_id=task_id, status="started")

@router.get("/analysis/status/{task_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(task_id: str, user: dict = Depends(require_auth)):
    if task_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis task not found")
    return AnalysisStatusResponse(**analysis_cache[task_id])

@router.get("/analysis/results/{task_id}")
async def get_analysis_results(task_id: str, user: dict = Depends(require_auth)) -> Dict[str, Any]:
    if task_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis task not found")

    cached = analysis_cache[task_id]
    if cached["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Analysis not completed. Status: {cached['status']}")

    return cached.get("result", {})

def run_analysis(session_id: str, task_id: str, db: Session):
    try:
        analysis_cache[task_id]["progress"] = 20
        error_detector = ErrorLogDetector(db)
        errors = error_detector.detect_errors(session_id)

        analysis_cache[task_id]["progress"] = 40
        call_chain_analyzer = CallChainAnalyzer(db)
        call_chain = call_chain_analyzer.analyze_call_chain(session_id, errors[0].timestamp if errors else None)

        analysis_cache[task_id]["progress"] = 60
        root_cause_analyzer = RootCauseAnalyzer()
        root_cause = root_cause_analyzer.analyze_root_cause(
            [{"level": e.level, "message": e.message, "timestamp": e.timestamp} for e in errors],
            call_chain
        )

        analysis_cache[task_id]["progress"] = 80
        issue_ranker = IssueRankingService()
        ranked_issues = issue_ranker.rank_issues([{"severity": e.level, "message": e.message, "probability": 0.8, "frequency": 1} for e in errors])

        perf_detector = PerformanceAnomalyDetector()
        anomalies = perf_detector.detect_anomalies([{"message": e.message} for e in errors])

        aggregator = AnalysisResultAggregator()
        result = aggregator.aggregate_results(root_cause, ranked_issues, anomalies, [])

        analysis_cache[task_id] = {"status": "completed", "progress": 100, "result": result}
    except Exception as e:
        analysis_cache[task_id] = {"status": "failed", "progress": 0, "error": str(e)}
