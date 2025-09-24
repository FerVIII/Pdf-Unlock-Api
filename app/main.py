import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request

from app.routers import unlock, health

# --- Cargar variables de entorno ---
load_dotenv()

# --- Configuración logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# --- Variables de seguridad ---
EXPECTED_TOKEN = "mi-token-secreto"
EXPECTED_CLIENT_ID = "cliente-1"

# --- Middleware de autenticación ---
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ignorar documentación de Swagger
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        client_id = request.headers.get("x-client-id")

        if not auth_header or not auth_header.lower().startswith("bearer "):
            return JSONResponse({"detail": "Authorization header missing"}, status_code=401)

        token = auth_header.split(" ", 1)[1].strip()
        if token != EXPECTED_TOKEN or client_id != EXPECTED_CLIENT_ID:
            return JSONResponse({"detail": "Invalid credentials"}, status_code=403)

        return await call_next(request)

# --- FastAPI ---
app = FastAPI(
    title="PDF Unlock API",
    description="API para desbloquear restricciones de PDFs protegidos por propietario.",
    version="1.1.0",
)

# --- Middleware ---
app.add_middleware(AuthMiddleware)
logger.info("Middleware de autenticación cargado.")

# --- Esquemas de seguridad para Swagger ---
bearer_scheme = HTTPBearer()
client_id_header = APIKeyHeader(name="X-Client-Id")

def get_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return credentials.credentials

def get_client_id(client_id: str = Depends(client_id_header)):
    return client_id

# --- Routers con dependencias para Swagger ---
app.include_router(unlock.router, dependencies=[Depends(get_token), Depends(get_client_id)])
logger.info("Router /unlock incluido.")

app.include_router(health.router, dependencies=[Depends(get_token), Depends(get_client_id)])
logger.info("Router /health incluido.")

logger.info("API PDF Unlock lista y funcionando.")
