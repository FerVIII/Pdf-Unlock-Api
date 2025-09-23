from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import tempfile
import os
import logging
from app.utils.pdf_tools import unlock_pdf
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@router.post("/unlock")
async def unlock_pdf_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        logger.warning(f"Archivo rechazado por tipo: {file.filename}")
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    # Guardar archivo de entrada temporalmente por chunks
    file_size = 0
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        while chunk := await file.read(1024*1024):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                tmp_in.close()
                os.remove(tmp_in.name)
                logger.warning(f"Archivo demasiado grande: {file.filename}")
                raise HTTPException(status_code=413, detail="Archivo demasiado grande")
            tmp_in.write(chunk)
    except Exception as e:
        tmp_in.close()
        os.remove(tmp_in.name)
        logger.error(f"Error leyendo el archivo {file.filename}: {e}")
        raise HTTPException(status_code=400, detail="Error procesando el archivo")
    finally:
        tmp_in.close()

    # Crear archivo de salida temporal
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_out.close()

    logger.info(f"Procesando PDF: {file.filename}, tamaño: {file_size} bytes")

    # Desbloquear PDF
    try:
        unlock_pdf(tmp_in.name, tmp_out.name)
    except ValueError as e:
        os.remove(tmp_in.name)
        os.remove(tmp_out.name)
        logger.error(f"No se pudo desbloquear {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        os.remove(tmp_in.name)
        os.remove(tmp_out.name)
        logger.error(f"Error inesperado {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar PDF")

    # Programar limpieza de archivos temporales
    background_tasks.add_task(os.remove, tmp_in.name)
    background_tasks.add_task(os.remove, tmp_out.name)

    # Devolver PDF desbloqueado
    return FileResponse(tmp_out.name, filename=f"desbloqueado_{file.filename}", media_type="application/pdf")
