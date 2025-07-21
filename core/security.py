from fastapi import Header, HTTPException, status
from app.core.config import settings

def api_key_auth(api_key: str = Header(...)):
    if api_key != settings.AI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )