from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from ..utils.pdf_tools import unlock_pdf
import os

router = APIRouter()

# Carpeta temporal para PDFs desbloqueados
UNLOCKED_DIR = "unlocked"
os.makedirs(UNLOCKED_DIR, exist_ok=True)

@router.post("/unlock")
async def unlock(file: UploadFile = File(...)):
    # Guardar archivo subido temporalmente
    temp_input_path = os.path.join(UNLOCKED_DIR, file.filename)
    with open(temp_input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Archivo desbloqueado
    unlocked_path = os.path.join(UNLOCKED_DIR, f"unlocked_{file.filename}")

    try:
        unlock_pdf(temp_input_path, unlocked_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error desbloqueando PDF: {e}")

    # Devolver PDF desbloqueado directamente
    return FileResponse(unlocked_path, filename=f"unlocked_{file.filename}", media_type="application/pdf")
