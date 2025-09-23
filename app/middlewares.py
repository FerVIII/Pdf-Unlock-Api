from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from .config import EXPECTED_TOKEN, EXPECTED_CLIENT_ID


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("authorization")
        client_id = request.headers.get("x-client-id")

        if not auth_header or not auth_header.lower().startswith("bearer "):
         return JSONResponse({"detail": "Authorization header missing"}, status_code=401)

        token = auth_header.split(" ", 1)[1].strip()
        if token != EXPECTED_TOKEN or client_id != EXPECTED_CLIENT_ID:
            return JSONResponse({"detail": "Invalid credentials"}, status_code=403)

        return await call_next(request)