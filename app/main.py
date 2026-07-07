#modularizar

from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from pydantic import BaseModel
import os

app = FastAPI(
    title="NovaRetail API",
    description="API de Backend para la Dicsys Data League - Exposición de KPIs",
    version="1.0.0"
)

try:
    client = bigquery.Client()
except Exception as e:
    print(f"Error al inicializar BigQuery. Verifica tus credenciales: {e}")

class KPIEjecutivo(BaseModel):
    ingresos_totales: float
    ganancia_neta: float
    ticket_promedio: float

class KPIOperativo(BaseModel):
    dias_envio_promedio: float
    total_pedidos_despachados: int

# Endpoints de la API

@app.get("/", tags=["Estado"])
def estado_api():
    return {"status": "online", "message": "API de NovaRetail funcionando correctamente."}


@app.get("/api/kpis/ejecutivo", response_model=KPIEjecutivo, tags=["KPIs"])
def obtener_kpis_ejecutivos():
    """
    Devuelve las métricas de alto nivel para el Dashboard Ejecutivo.
    """
    query = """
        SELECT 
            SUM(revenue) as ingresos_totales,
            SUM(profit) as ganancia_neta,
            SUM(revenue) / COUNT(DISTINCT order_id) as ticket_promedio
        FROM `dataleaguenovaretail.nV_core_datasets.FACT_SALES`
    """
    
    try:
        query_job = client.query(query)
        resultados = query_job.result()
        
        for fila in resultados:
            return {
                "ingresos_totales": round(fila.ingresos_totales, 2) if fila.ingresos_totales else 0,
                "ganancia_neta": round(fila.ganancia_neta, 2) if fila.ganancia_neta else 0,
                "ticket_promedio": round(fila.ticket_promedio, 2) if fila.ticket_promedio else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/kpis/operativo", response_model=KPIOperativo, tags=["KPIs"])
def obtener_kpis_operativos():
    """
    Devuelve las métricas logísticas para el Dashboard Operativo.
    """
    query = """
        SELECT 
            AVG(DATE_DIFF(delivery_date, shipment_date, DAY)) as dias_envio_promedio,
            COUNT(DISTINCT shipment_id) as total_pedidos_despachados
        FROM `dataleaguenovaretail.nV_core_datasets.DIM_SHIPPING`
    """
    
    try:
        query_job = client.query(query)
        resultados = query_job.result()
        
        for fila in resultados:
            return {
                "dias_envio_promedio": round(fila.dias_envio_promedio, 2) if fila.dias_envio_promedio else 0,
                "total_pedidos_despachados": fila.total_pedidos_despachados if fila.total_pedidos_despachados else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))