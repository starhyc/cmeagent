from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_admin
from app.models.database import SSHServer
from app.services.credentials import credential_manager
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SSHServerCreate(BaseModel):
    name: str
    host: str
    port: int = 22
    username: str
    password: str
    log_path: str = None

class SSHServerResponse(BaseModel):
    id: int
    name: str
    host: str
    port: int
    username: str
    log_path: str = None

    class Config:
        from_attributes = True

@router.post("/ssh-servers", response_model=SSHServerResponse)
def create_ssh_server(server: SSHServerCreate, db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    encrypted_password = credential_manager.encrypt(server.password)
    new_server = SSHServer(
        name=server.name,
        host=server.host,
        port=server.port,
        username=server.username,
        encrypted_password=encrypted_password,
        log_path=server.log_path
    )
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@router.get("/ssh-servers", response_model=List[SSHServerResponse])
def list_ssh_servers(db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    return db.query(SSHServer).all()

@router.delete("/ssh-servers/{server_id}")
def delete_ssh_server(server_id: int, db: Session = Depends(get_db), _: dict = Depends(require_admin)):
    server = db.query(SSHServer).filter(SSHServer.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"message": "Server deleted"}
