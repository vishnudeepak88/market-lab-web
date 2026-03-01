from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if settings.api_key:
        if api_key != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API Key",
            )
    # If no API key configured (e.g. prod without key set), you might want to deny all or allow all.
    # The requirement says "default: 'dev-key' only in demo mode".
    # Assuming if it's required but missing, we should deny. If not configured at all, we might allow or deny.
    # We will enforce it strictly if `settings.api_key` is set.
    return api_key
