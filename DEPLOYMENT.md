# Problem Diagnosis Assistant - Deployment Guide

## Prerequisites

- Python 3.9+
- Node.js 16+
- Pandoc and XeLaTeX for PDF generation
- SQLite 3

## Backend Deployment

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.template .env
# Edit .env with your configuration
```

3. Generate Fernet key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

4. Initialize database:
```bash
python -m app.scripts.init_db
```

5. Create admin user:
```bash
python -m app.scripts.create_admin
```

6. Start server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Frontend Deployment

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Build for production:
```bash
npm run build
```

3. Serve static files (configure backend to serve from dist/)

## System Requirements

- 4GB RAM minimum
- 20GB disk space for logs and reports
- Network access to SSH servers
- Access to LLM endpoint

## Security Checklist

- [ ] Set strong JWT_SECRET
- [ ] Rotate Fernet encryption key regularly
- [ ] Restrict file permissions on .env
- [ ] Configure firewall rules
- [ ] Enable HTTPS in production
- [ ] Review audit logs regularly

## Monitoring

- Check /health endpoint for service status
- Monitor disk usage in LOG_STORAGE_PATH and REPORT_STORAGE_PATH
- Review error logs in application logs
