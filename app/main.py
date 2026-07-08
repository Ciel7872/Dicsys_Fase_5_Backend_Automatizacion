from fastapi import FastAPI, HTTPException, Depends
from app.schemas import KPIEjecutivo, KPIOperativo
from app.database import obtener_cliente_bigquery

app = FastAPI(
    title="NovaRetail API",
    description="API de Backend para la Dicsys Data League - Exposición de KPIs",
    version="1.0.0"
)

@app.get("/", tags=["Estado"])
def estado_api():
    return {"status": "online", "message": "API de NovaRetail funcionando correctamente."}


@app.get("/api/kpis/ejecutivo", response_model=KPIEjecutivo, tags=["KPIs"])
def obtener_kpis_ejecutivos(client=Depends(obtener_cliente_bigquery)):
    """Devuelve las métricas de alto nivel para el Dashboard Ejecutivo."""
    query = """
        SELECT 
            SUM(revenue) as ingresos_totales,
            SUM(profit) as ganancia_neta,
            SUM(revenue) / COUNT(DISTINCT order_id) as ticket_promedio
        FROM `dataleaguenovaretail.nv_core_datasets.FACT_SALES`
    """
    try:
        query_job = client.query(query, location="us-south1")
        fila = list(query_job.result())[0]  # Al ser agregación, sabemos que trae 1 sola fila
        
        return {
            "ingresos_totales": round(fila.ingresos_totales, 2) if fila.ingresos_totales else 0,
            "ganancia_neta": round(fila.ganancia_neta, 2) if fila.ganancia_neta else 0,
            "ticket_promedio": round(fila.ticket_promedio, 2) if fila.ticket_promedio else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Query Ejecutivo: {str(e)}")


@app.get("/api/kpis/operativo", response_model=KPIOperativo, tags=["KPIs"])
def obtener_kpis_operativos(client=Depends(obtener_cliente_bigquery)):
    """Devuelve las métricas logísticas completas para el Dashboard Operativo."""
    query = """
        SELECT 
            AVG(DATE_DIFF(delivery_date, shipment_date, DAY)) as dias_envio_promedio,
            COUNT(DISTINCT shipment_id) as total_pedidos_despachados,
            COUNTIF(DATE_DIFF(delivery_date, shipment_date, DAY) > 4) as envios_demorados,
            AVG(cost) as costo_envio_promedio
        FROM `dataleaguenovaretail.nv_core_datasets.DIM_SHIPPING`
    """
    try:
        query_job = client.query(query, location="us-south1")
        fila = list(query_job.result())[0]
        
        return {
            "dias_envio_promedio": round(fila.dias_envio_promedio, 2) if fila.dias_envio_promedio else 0,
            "total_pedidos_despachados": fila.total_pedidos_despachados if fila.total_pedidos_despachados else 0,
            "envios_demorados": fila.envios_demorados if fila.envios_demorados else 0,
            "costo_envio_promedio": round(fila.costo_envio_promedio, 2) if fila.costo_envio_promedio else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Query Operativo: {str(e)}")