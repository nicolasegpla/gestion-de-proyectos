from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistoriaUsuarioBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "pendiente"   # pendiente, en_progreso, completado
    prioridad: Optional[str] = "media"    # baja, media, alta

class HistoriaUsuarioCreate(HistoriaUsuarioBase):
    proyecto_id: int

class HistoriaUsuarioResponse(HistoriaUsuarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
