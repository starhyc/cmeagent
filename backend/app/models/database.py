from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False)
    source = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    level = Column(String(20))
    module = Column(String(100))
    message = Column(Text)
    raw_content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(255))
    details = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

class SSHServer(Base):
    __tablename__ = "ssh_servers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, default=22)
    username = Column(String(100), nullable=False)
    encrypted_password = Column(Text)
    log_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    markdown_path = Column(String(500), nullable=False)
    pdf_path = Column(String(500))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
