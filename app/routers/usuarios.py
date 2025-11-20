# app/api/v1/endpoints/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.empresa import Empresa
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.core.security import hash_password, create_access_token, verify_password
from app.schemas.usuario import UsuarioCreate, LoginRequest

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Validar que la empresa exista y esté activa
    empresa = db.query(Empresa).filter(
        Empresa.id == data.empresa_id,
        Empresa.activa == True
    ).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada o inactiva")

    # 2. Validar que el correo del usuario no exista
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El correo ya está en uso")

    # 3. Crear el usuario
    nuevo_usuario = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
        rol=data.rol,
        empresa_id=data.empresa_id,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 4. Crear token de acceso (JWT)
    token_data = {
        "sub": nuevo_usuario.email,
        "id": nuevo_usuario.id,
        "rol": nuevo_usuario.rol
    }
    access_token = create_access_token(data=token_data)

    # 5. Retornar usuario + token
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "rol": nuevo_usuario.rol,
                "empresa_id": nuevo_usuario.empresa_id,
                "activo": nuevo_usuario.activo
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    )


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not usuario.activo:
        raise HTTPException(status_code=403, detail="El usuario está inactivo")

    # Verificar contraseña
    if not verify_password(data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 🔥 Generar token JWT con type="usuario"
    token_data = {
        "sub": usuario.email,
        "id": usuario.id,
        "rol": usuario.rol,
        "empresa_id": usuario.empresa_id,
        "type": "usuario"     # 👈 NECESARIO PARA get_current_actor
    }

    access_token = create_access_token(data=token_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "empresa_id": usuario.empresa_id,
                "activo": usuario.activo
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
