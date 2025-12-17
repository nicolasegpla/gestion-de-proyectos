from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# 🧩 Base Schema (campos comunes)
class EmpresaBase(BaseModel):
    nombre: str = Field(..., example="Distrines Ltda")
    email_contacto: Optional[EmailStr] = Field(None, example="contacto@distrines.com")


# 🧾 Schema para creación (registro inicial)
class EmpresaCreate(EmpresaBase):
    password: str = Field(..., min_length=6, example="123456")


# 🔑 Schema para login
class EmpresaLogin(BaseModel):
    email_contacto: EmailStr
    password: str


# 🛠️ Schema para actualización
class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    activa: Optional[bool] = None


# 📤 Schema de respuesta (sin exponer contraseña)
class EmpresaResponse(EmpresaBase):
    id: int
    activa: bool
    fecha_registro: Optional[datetime] = None
    creada_en: Optional[datetime] = None
    actualizada_en: Optional[datetime] = None
    tipo_suscripcion: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Distrines Ltda",
                "email_contacto": "contacto@distrines.com",
                "activa": True,
                "fecha_registro": "2025-10-25T10:00:00Z",
                "tipo_suscripcion": "gratuita",
            }
        }

# app/schemas/empresa.py
class EmpresaListResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
