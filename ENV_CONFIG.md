# Environment Variable Configuration

## Required Variables

### LLM Configuration
- `LLM_ENDPOINT`: URL of the OpenAI-compatible LLM endpoint (e.g., `http://localhost:8000/v1`)
- `LLM_API_KEY`: API key for the LLM endpoint
- `LLM_MODEL`: Model name to use for embeddings and analysis

### Security
- `FERNET_KEY`: Encryption key for SSH credentials (generate with `Fernet.generate_key()`)
- `JWT_SECRET`: Secret key for JWT token generation (use a strong random string)
- `JWT_ALGORITHM`: JWT algorithm (default: `HS256`)
- `JWT_EXPIRE_MINUTES`: Session timeout in minutes (default: `30`)

### Database
- `DATABASE_PATH`: Path to SQLite database file (e.g., `./data/app.db`)

### Storage
- `LOG_STORAGE_PATH`: Directory for storing uploaded log files (e.g., `./data/logs`)
- `REPORT_STORAGE_PATH`: Directory for storing generated reports (e.g., `./data/reports`)
- `CODE_INDEX_PATH`: Directory for ChromaDB code index (e.g., `./data/code_index`)

## Generating Secure Keys

### Fernet Key
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### JWT Secret
```bash
openssl rand -hex 32
```

## Example Configuration

```bash
LLM_ENDPOINT=http://internal-llm.company.com/v1
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4

FERNET_KEY=your-generated-fernet-key-here
JWT_SECRET=your-generated-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

DATABASE_PATH=./data/app.db
LOG_STORAGE_PATH=./data/logs
REPORT_STORAGE_PATH=./data/reports
CODE_INDEX_PATH=./data/code_index
```

## Security Best Practices

1. Never commit `.env` file to version control
2. Rotate keys regularly (quarterly recommended)
3. Use different keys for development and production
4. Restrict file permissions: `chmod 600 .env`
5. Store production keys in secure key management system
