import pikepdf


def unlock_pdf(input_path: str, output_path: str):
    """
    Abre un PDF aunque tenga restricciones de propietario
    (copiar, imprimir, editar) y lo guarda sin restricciones.
    """
    pdf = pikepdf.Pdf.open(input_path)
    pdf.save(output_path)
    pdf.close()