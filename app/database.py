from google.cloud import bigquery
from fastapi import HTTPException

def obtener_cliente_bigquery():
    """Inicializa y devuelve el cliente de BigQuery de forma segura."""
    try:
        # Busca automáticamente la variable GOOGLE_APPLICATION_CREDENTIALS
        return bigquery.Client()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error crítico de infraestructura al conectar con BigQuery: {str(e)}"
        )