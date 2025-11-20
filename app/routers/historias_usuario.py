from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.proyecto import Proyecto
from app.models.historia_usuario import HistoriaUsuario
from app.schemas.historia_usuario import HistoriaUsuarioCreate, HistoriaUsuarioResponse, HistoriaUsuarioBase
from app.core.deps import get_current_empresa

router = APIRouter(prefix="/historias-usuario", tags=["Historias de Usuario"])


@router.post("/", response_model=HistoriaUsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_historia(data: HistoriaUsuarioCreate, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    proyecto = db.query(Proyecto).filter_by(id=data.proyecto_id, empresa_id=empresa_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o no pertenece a tu empresa")

    historia = HistoriaUsuario(
        proyecto_id=data.proyecto_id,
        titulo=data.titulo,
        descripcion=data.descripcion,
        estado=data.estado,
        prioridad=data.prioridad
    )
    db.add(historia)
    db.commit()
    db.refresh(historia)
    return historia


@router.get("/proyecto/{proyecto_id}", response_model=List[HistoriaUsuarioResponse])
def listar_por_proyecto(proyecto_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    proyecto = db.query(Proyecto).filter_by(id=proyecto_id, empresa_id=empresa_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o no pertenece a tu empresa")

    historias = db.query(HistoriaUsuario).filter_by(proyecto_id=proyecto_id).all()
    return historias


@router.get("/{historia_id}", response_model=HistoriaUsuarioResponse)
def obtener_historia(historia_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    historia = db.query(HistoriaUsuario).join(Proyecto).filter(HistoriaUsuario.id == historia_id).first()

    if not historia or historia.proyecto.empresa_id != getattr(current_actor, "empresa_id", current_actor.id):
        raise HTTPException(status_code=404, detail="Historia no encontrada o no pertenece a tu empresa")

    return historia


@router.put("/{historia_id}", response_model=HistoriaUsuarioResponse)
def actualizar_historia(historia_id: int, data: HistoriaUsuarioBase, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    historia = db.query(HistoriaUsuario).join(Proyecto).filter(HistoriaUsuario.id == historia_id).first()

    if not historia or historia.proyecto.empresa_id != getattr(current_actor, "empresa_id", current_actor.id):
        raise HTTPException(status_code=404, detail="Historia no encontrada o no pertenece a tu empresa")

    historia.titulo = data.titulo
    historia.descripcion = data.descripcion
    historia.estado = data.estado
    historia.prioridad = data.prioridad
    db.commit()
    db.refresh(historia)
    return historia


@router.delete("/{historia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_historia(historia_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    historia = db.query(HistoriaUsuario).join(Proyecto).filter(HistoriaUsuario.id == historia_id).first()

    if not historia or historia.proyecto.empresa_id != getattr(current_actor, "empresa_id", current_actor.id):
        raise HTTPException(status_code=404, detail="Historia no encontrada o no pertenece a tu empresa")

    db.delete(historia)
    db.commit()
