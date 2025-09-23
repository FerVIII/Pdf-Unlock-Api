from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile, os
from ..utils.pdf_tools import unlock_pdf

router = APIRouter()


@router.post("/unlock")
async def unlock(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
       raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")


    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_in.write(await file.read())
    tmp_in.close()


    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_out.close()


    try:
        unlock_pdf(tmp_in.name, tmp_out.name)
        return FileResponse(tmp_out.name, media_type="application/pdf", filename=f"unlocked_{file.filename}")
    finally:
        os.remove(tmp_in.name)
     