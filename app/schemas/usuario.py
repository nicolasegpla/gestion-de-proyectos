from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str  # La encriptarás en el endpoint
    rol: Optional[str] = "cobrador"
    empresa_id: int  # Proporcionado al crear el usuario

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool

    class Config:
        from_attributes = True  # antes orm_mode



