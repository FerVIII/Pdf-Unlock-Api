from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.utils.pdf_tools import unlock_pdf
import shutil
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
UNLOCKED_DIR = "unlocked"

# Aseguramos directorios
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(UNLOCKED_DIR, exist_ok=True)

@router.post("/unlock")
async def unlock_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Recibe un PDF con restricciones de propietario y devuelve una copia desbloqueada.
    Middleware valida Authorization y X-Client-Id.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(UNLOCKED_DIR, file.filename)

    # Guardamos el archivo subido
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Desbloqueamos en background si quieres (opcional)
    if background_tasks:
        background_tasks.add_task(unlock_pdf, input_path, output_path)
    else:
        unlock_pdf(input_path, output_path)

    logger.info(f"PDF desbloqueado: {file.filename}")
    return {"message": "PDF desbloqueado correctamente", "unlocked_file": output_path}
