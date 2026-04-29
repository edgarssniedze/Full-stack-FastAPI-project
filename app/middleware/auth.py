from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import decode_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        token = request.cookies.get("token")

        request.state.user = None 

        if token:
            try:
                payload = decode_token(token)
                request.state.user = payload
            except Exception:
                request.state.user = None

        return await call_next(request)