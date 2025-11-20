from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.models.proyecto import Proyecto
from app.models.historia_usuario import HistoriaUsuario
from app.models.ticket import Ticket


# Exporta los modelos para que Alembic los vea
__all__ = ["Empresa", "Usuario", "Proyecto", "HistoriaUsuario", "Ticket"]
