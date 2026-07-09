# NovaRetail API - Backend KPIs

API REST modular desarrollada en **Python (FastAPI)** para la extracción y exposición de KPIs clave (Ejecutivos y Operativos) directamente desde BigQuery para la **Dicsys Data League**.

## 📁 Estructura del Proyecto

```text
Dicsys_Fase_5_Backend_Automatizacion/
├── app/
│   ├── __init__.py
│   ├── database.py      # Inicialización segura del cliente BigQuery
│   ├── main.py          # Endpoints y lógica de queries SQL
│   └── schemas.py       # Modelos de validación de datos (Pydantic)
├── .gitignore           # Archivos omitidos (evita subir credenciales)
├── gcp-credentials.json # Tu llave de GCP (Ignorada en Git por seguridad)
├── README.md            # Documentación del proyecto
└── requirements.txt     # Dependencias del proyecto



1. Clonar el repositorio y crear Entorno Virtual
Abrí la terminal en la raíz del proyecto y ejecutá: 
windows: python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1

linux: python3 -m venv .venv
source .venv/bin/activate

2. Instalar dependencias
Con el entorno virtual activo (.venv), instalá los paquetes necesarios:
pip install -r requirements.txt

3. Credenciales de Google Cloud (gcp-credentials.json)
⚠️ IMPORTANTE: Por razones de seguridad, las llaves privadas no se suben al repositorio.

Solicitá el archivo de la cuenta de servicio con el rol de Administrador de BigQuery.

Guardá el archivo en la raíz del proyecto con el nombre exacto: gcp-credentials.json.

🚀 Ejecución de la API
Con el entorno virtual activo y el archivo de credenciales en su lugar, ejecutá los comandos según tu terminal:
$env:GOOGLE_APPLICATION_CREDENTIALS="gcp-credentials.json"
python -m uvicorn app.main:app --reload

linux : export GOOGLE_APPLICATION_CREDENTIALS="gcp-credentials.json"
python3 -m uvicorn app.main:app --reload

http://127.0.0.1:8000/docs  -> agregar docs al final para visualizar