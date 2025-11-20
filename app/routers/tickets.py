from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.historia_usuario import HistoriaUsuario
from app.schemas.ticket import TicketCreate, TicketResponse, TicketBase, TicketEstadoUpdate
from app.core.deps import get_current_empresa

router = APIRouter(prefix="/tickets", tags=["Tickets"])

# Crear un ticket
@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def crear_ticket(data: TicketCreate, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    historia = db.query(HistoriaUsuario).filter(HistoriaUsuario.id == data.historia_usuario_id).first()

    if not historia:
        raise HTTPException(status_code=404, detail="Historia de usuario no encontrada")

    if historia.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta historia de usuario")

    nuevo_ticket = Ticket(
        historia_usuario_id=data.historia_usuario_id,
        asunto=data.asunto,
        descripcion=data.descripcion,
        estado=data.estado,
        prioridad=data.prioridad,
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket


# Listar tickets por historia de usuario
@router.get("/historia/{historia_usuario_id}", response_model=List[TicketResponse])
def listar_tickets_por_historia(historia_usuario_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    historia = db.query(HistoriaUsuario).filter(HistoriaUsuario.id == historia_usuario_id).first()
    if not historia:
        raise HTTPException(status_code=404, detail="Historia de usuario no encontrada")

    if historia.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estos tickets")

    return historia.tickets


# Obtener un ticket específico
@router.get("/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(ticket_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.historia_usuario.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este ticket")

    return ticket


# Eliminar un ticket
@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.historia_usuario.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este ticket")

    db.delete(ticket)
    db.commit()

# Actualizar un ticket
@router.put("/{ticket_id}", response_model=TicketResponse)
def actualizar_ticket(ticket_id: int, data: TicketBase, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.historia_usuario.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este ticket")

    # Actualizar campos
    ticket.asunto = data.asunto
    ticket.descripcion = data.descripcion
    ticket.estado = data.estado
    ticket.prioridad = data.prioridad

    db.commit()
    db.refresh(ticket)
    return ticket

# Actualizar el estado de un ticket
@router.patch("/{ticket_id}/estado", response_model=TicketResponse)
def actualizar_estado_ticket(ticket_id: int, data: TicketEstadoUpdate, db: Session = Depends(get_db), current_actor=Depends(get_current_empresa)):
    empresa_id = getattr(current_actor, "empresa_id", current_actor.id)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.historia_usuario.proyecto.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este ticket")

    ticket.estado = data.estado

    db.commit()
    db.refresh(ticket)
    return ticket

