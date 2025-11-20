from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_actor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    empresa = db.query(Empresa).filter(Empresa.email_contacto == email).first()
    if empresa is None:
        raise credentials_exception
    return empresa


def get_current_empresa(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        entity_type = payload.get("type")
        entity_id = payload.get("id")
        email = payload.get("sub")

        if entity_type == "empresa":
            empresa = db.query(Empresa).filter(Empresa.id == entity_id, Empresa.email_contacto == email).first()
            if not empresa or not empresa.activa:
                raise credentials_exception
            return empresa

        elif entity_type == "usuario":
            usuario = db.query(Usuario).filter(Usuario.id == entity_id, Usuario.email == email).first()
            if not usuario or not usuario.activo:
                raise credentials_exception
            return usuario

        raise credentials_exception

    except JWTError:
        raise credentials_exception