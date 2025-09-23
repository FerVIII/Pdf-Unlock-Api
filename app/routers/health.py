from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

API_VERSION = "1.1.0"

@router.get("/health")
async def health():
    logger.info("Chequeo de estado /health recibido")
    return {"status": "ok", "version": API_VERSION}
