from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.security import decode_access_token
from app.models.database import UserRole

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_access_token(credentials.credentials)
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_auth(user: dict = Depends(get_current_user)):
    return user

async def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
