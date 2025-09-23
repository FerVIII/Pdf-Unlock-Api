from fastapi import FastAPI
from .middlewares import AuthMiddleware
from app.routers import unlock, health
import logging
from dotenv import load_dotenv

load_dotenv()  # carga variables de .env automáticamente




logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Unlock API",
    description="API para desbloquear restricciones de PDFs protegidos por propietario.",
    version="1.1.0"
)

app.add_middleware(AuthMiddleware)
logger.info("Middleware de autenticación cargado.")

app.include_router(unlock.router)
logger.info("Router /unlock incluido.")
app.include_router(health.router)
logger.info("Router /health incluido.")

logger.info("API PDF Unlock lista y funcionando.")
