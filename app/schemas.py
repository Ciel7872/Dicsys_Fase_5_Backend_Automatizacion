from pydantic import BaseModel

class KPIEjecutivo(BaseModel):
    ingresos_totales: float
    ganancia_neta: float
    ticket_promedio: float

class KPIOperativo(BaseModel):
    dias_envio_promedio: float
    total_pedidos_despachados: int
    envios_demorados: int
    costo_envio_promedio: float