import os
import logging

# Configuración de logging básico
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Tokens y Client ID desde variables de entorno
EXPECTED_TOKEN = os.getenv("API_TOKEN")
EXPECTED_CLIENT_ID = os.getenv("CLIENT_ID")

# Validación mínima: avisar si no están configurados
if not EXPECTED_TOKEN or not EXPECTED_CLIENT_ID:
    logging.warning(
        "No se encontraron variables de entorno API_TOKEN o CLIENT_ID. "
        "Usando valores por defecto para desarrollo."
    )
    EXPECTED_TOKEN = EXPECTED_TOKEN or "mi-token-secreto"
    EXPECTED_CLIENT_ID = EXPECTED_CLIENT_ID or "cliente-1"
