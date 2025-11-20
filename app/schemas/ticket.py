from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketEstadoUpdate(BaseModel):
    estado: str

class TicketBase(BaseModel):
    asunto: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "abierto"     # abierto, en_progreso, cerrado
    prioridad: Optional[str] = "media"    # baja, media, alta

class TicketCreate(TicketBase):
    historia_usuario_id: int

class TicketResponse(TicketBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
