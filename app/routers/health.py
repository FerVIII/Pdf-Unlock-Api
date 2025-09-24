from fastapi import APIRouter, Depends
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

API_VERSION = "1.1.0"

@router.get("/health")
async def health():
    """
    Endpoint de chequeo de estado.
    Middleware valida Authorization y X-Client-Id.
    """
    logger.info("Chequeo de estado /health recibido")
    return {"status": "ok", "version": API_VERSION}
