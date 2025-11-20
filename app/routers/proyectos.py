from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.proyecto import Proyecto
from app.models.historia_usuario import HistoriaUsuario
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse, ProyectoBase
from app.schemas.historia_usuario import HistoriaUsuarioResponse
from app.core.deps import get_current_empresa

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def crear_proyecto(data: ProyectoCreate, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    nuevo_proyecto = Proyecto(
        nombre=data.nombre,
        descripcion=data.descripcion,
        empresa_id=empresa_id  # ✅ se extrae del token
    )
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto


@router.get("/", response_model=list[ProyectoResponse])
def listar_proyectos(db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)
    return db.query(Proyecto).filter(Proyecto.empresa_id == empresa_id).all()


@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id, empresa_id=empresa_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto(proyecto_id: int, data: ProyectoBase, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id, empresa_id=empresa_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto.nombre = data.nombre
    proyecto.descripcion = data.descripcion
    db.commit()
    db.refresh(proyecto)
    return proyecto

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)
    proyecto = db.query(Proyecto).filter_by(id=proyecto_id, empresa_id=empresa_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    db.delete(proyecto)
    db.commit()
