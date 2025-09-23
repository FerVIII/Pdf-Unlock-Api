from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from .config import EXPECTED_TOKEN, EXPECTED_CLIENT_ID
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("authorization")
        client_id = request.headers.get("x-client-id")

        if not auth_header or not auth_header.lower().startswith("bearer "):
            logger.warning(f"Intento de acceso sin token desde {request.client.host}")
            return JSONResponse({"detail": "Authorization header missing"}, status_code=401)

        token = auth_header.split(" ", 1)[1].strip()
        if token != EXPECTED_TOKEN or client_id != EXPECTED_CLIENT_ID:
            logger.warning(f"Intento de acceso inválido desde {request.client.host}")
            return JSONResponse({"detail": "Invalid credentials"}, status_code=403)

        logger.info(f"Acceso autorizado desde {request.client.host}")
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error interno al procesar la solicitud: {e}")
            return JSONResponse({"detail": "Internal server error"}, status_code=500)
