import pikepdf
import logging

logger = logging.getLogger(__name__)

def unlock_pdf(input_path: str, output_path: str):
    try:
        pdf = pikepdf.Pdf.open(input_path)
        pdf.save(output_path)
        pdf.close()
        logger.info(f"PDF desbloqueado correctamente: {input_path} -> {output_path}")
    except pikepdf._qpdf.PasswordError:
        logger.error(f"PDF protegido por contraseña: {input_path}")
        raise ValueError("PDF protegido por contraseña, no se puede desbloquear.")
    except Exception as e:
        logger.error(f"Error al procesar el PDF {input_path}: {e}")
        raise ValueError("PDF inválido o corrupto.")
