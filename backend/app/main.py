from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, users, logs, ssh_servers, analysis, code, reports
from app.core.database import init_db
import os

app = FastAPI(title="Problem Diagnosis Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(ssh_servers.router, prefix="/api", tags=["ssh-servers"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(code.router, prefix="/api", tags=["code"])
app.include_router(reports.router, prefix="/api", tags=["reports"])

frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

