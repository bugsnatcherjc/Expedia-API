from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if session exists in cookies
        session_id = request.cookies.get("session_id")
        
        if not session_id:
            # Generate new session ID
            session_id = str(uuid.uuid4())
        
        # Add session_id to request state
        request.state.session_id = session_id
        
        # Process request
        response = await call_next(request)
        
        # Set session cookie in response
        response.set_cookie(
            key="session_id", 
            value=session_id,
            max_age=30 * 24 * 60 * 60,  # 30 days
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        return response
