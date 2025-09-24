import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Security
from fastapi.security import HTTPBearer, APIKeyHeader

from .middlewares import AuthMiddleware
from app.routers import unlock, health

# --- Configuración base ---
load_dotenv()  # carga variables de entorno desde .env

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Unlock API",
    description="API para desbloquear restricciones de PDFs protegidos por propietario.",
    version="1.1.0"
)

# --- Middleware global ---
app.add_middleware(AuthMiddleware)
logger.info("Middleware de autenticación cargado.")

# --- Seguridad para Swagger ---
bearer_scheme = HTTPBearer(auto_error=False)
client_id_header = APIKeyHeader(name="X-Client-Id", auto_error=False)

# Dependencias para Swagger
def get_bearer_token(credentials: HTTPBearer = Security(bearer_scheme)):
    return credentials.credentials if credentials else None

def get_client_id(client_id: str = Security(client_id_header)):
    return client_id

# --- Routers ---
# Swagger pedirá token y X-Client-Id, middleware valida realmente
app.include_router(
    unlock.router,
    dependencies=[Depends(get_bearer_token), Depends(get_client_id)]
)
logger.info("Router /unlock incluido.")

app.include_router(
    health.router,
    dependencies=[Depends(get_bearer_token), Depends(get_client_id)]
)
logger.info("Router /health incluido.")

logger.info("API PDF Unlock lista y funcionando.")
