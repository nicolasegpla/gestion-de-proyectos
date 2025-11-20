from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class ProyectoCreate(ProyectoBase):
    nombre: str
    descripcion: Optional[str] = None

class ProyectoResponse(ProyectoBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
