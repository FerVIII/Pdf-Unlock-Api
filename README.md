# PDF Unlock API

API para desbloquear restricciones de PDFs protegidos por propietario (copiar, imprimir, editar).  
No afecta PDFs protegidos con contraseña de apertura, solo restricciones de propietario.

---

## Requisitos

Python 3.10+  
Instala dependencias:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

O con conda:

\`\`\`bash
conda create -n api_pdf python=3.10
conda activate api_pdf
pip install -r requirements.txt
\`\`\`

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

\`\`\`env
API_TOKEN=mi-token-secreto
CLIENT_ID=cliente-1
\`\`\`

Si no existen, se usarán valores por defecto para desarrollo.

---

## Estructura

\`\`\`
app/
├── main.py # Entrada de la API
├── middlewares.py # Middleware de autenticación
├── routers/
│ ├── health.py # Endpoint /health
│ └── unlock.py # Endpoint /unlock
└── utils/
└── pdf_tools.py # Función unlock_pdf
uploads/ # Archivos PDF subidos
unlocked/ # Archivos PDF desbloqueados
\`\`\`

---

## Ejecutar localmente

\`\`\`bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
\`\`\`

La API estará disponible en:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

---

## Endpoints

### 1. Health check

\`\`\`http
GET /health
Headers:
Authorization: Bearer <API_TOKEN>
X-Client-Id: <CLIENT_ID>
\`\`\`

Respuesta:

\`\`\`json
{
"status": "ok",
"version": "1.1.0"
}
\`\`\`

---

### 2. Unlock PDF

\`\`\`http
POST /unlock
Headers:
Authorization: Bearer <API_TOKEN>
X-Client-Id: <CLIENT_ID>
Form-data:
file: <archivo.pdf>
\`\`\`

Respuesta:

\`\`\`json
{
"message": "PDF desbloqueado correctamente",
"unlocked_file": "unlocked/<archivo.pdf>"
}
\`\`\`

---

## Curl de prueba

\`\`\`bash
curl -X POST "http://127.0.0.1:8000/unlock" \
 -H "Authorization: Bearer mi-token-secreto" \
 -H "X-Client-Id: cliente-1" \
 -F "file=@/ruta/a/mi.pdf" \
 --output desbloqueado.pdf
\`\`\`

---

## Notas

- La API desbloquea restricciones de propietario sin necesidad de contraseña.
- Las validaciones de seguridad están manejadas por el middleware global.
- `/docs` permite usar el botón **Authorize** para probar token y client-id.
  EOF
