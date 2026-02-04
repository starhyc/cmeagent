from fastapi import APIRouter, Depends
from app.core.auth import require_auth
from app.services.code.index_db import CodeIndexDB
from app.services.code.indexing_service import CodeIndexingService
from app.services.code.explanation_service import CodeExplanationService
from pydantic import BaseModel
from typing import List

router = APIRouter()

class CodeSearchRequest(BaseModel):
    query: str
    n_results: int = 5

class CodeSearchResult(BaseModel):
    file_path: str
    content: str
    start_line: int
    end_line: int
    distance: float

class CodeExplanationRequest(BaseModel):
    code: str
    language: str

class CodeExplanationResponse(BaseModel):
    explanation: str

@router.post("/code/search", response_model=List[CodeSearchResult])
async def search_code(request: CodeSearchRequest, user: dict = Depends(require_auth)):
    indexing_service = CodeIndexingService()
    query_embedding = indexing_service._generate_embeddings([request.query])[0]

    index_db = CodeIndexDB()
    results = index_db.search(query_embedding, request.n_results)

    return [
        CodeSearchResult(
            file_path=meta['file_path'],
            content=doc,
            start_line=meta['start_line'],
            end_line=meta['end_line'],
            distance=dist
        )
        for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
    ]

@router.post("/code/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest, user: dict = Depends(require_auth)):
    explanation_service = CodeExplanationService()
    explanation = explanation_service.explain_code(request.code, request.language)
    return CodeExplanationResponse(explanation=explanation)
