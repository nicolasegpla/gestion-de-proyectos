from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.services.empresa import autenticar_empresa, crear_empresa
from app.schemas.empresa import EmpresaCreate, EmpresaLogin, EmpresaResponse
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.empresa import Empresa
router = APIRouter(prefix="/auth", tags=["Autenticación Empresa"])
from typing import List
from app.schemas.empresa import EmpresaListResponse


@router.post("/registro", response_model=EmpresaResponse)
def registro_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    empresa_existente = db.query(Empresa).filter(Empresa.email_contacto == data.email_contacto).first()
    if empresa_existente:
        raise HTTPException(status_code=400, detail="Ya existe una empresa con este correo.")
    empresa = crear_empresa(db, data)
    return empresa


@router.post("/login")
def login_empresa(data: EmpresaLogin, db: Session = Depends(get_db)):
    empresa = autenticar_empresa(db, data.email_contacto, data.password)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        data={
            "sub": empresa.email_contacto,
            "id": empresa.id,
            "type": "empresa"  # 👈 Obligatorio para autenticación unificada
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "empresa_id": empresa.id,
        "empresa_nombre": empresa.nombre
    }


@router.get("/listado-empresas", response_model=List[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    return empresas

@router.get("/resumen", response_model=List[EmpresaListResponse])
def obtener_lista_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa.id, Empresa.nombre).all()
    return [{"id": e.id, "nombre": e.nombre} for e in empresas]
