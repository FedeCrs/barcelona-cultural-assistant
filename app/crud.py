from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate
from sqlalchemy import or_
from app import models
from datetime import datetime


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def search_espacios_por_nombre_o_direccion(db: Session, texto: str):
    """
    Busca espacios por nombre o dirección usando coincidencia parcial (LIKE),
    case-insensitive, para que funcione aunque el usuario agregue palabras extra.
    """
    texto_like = f"%{texto}%"
    resultados = db.query(models.Usuario).filter(
        or_(
            models.Usuario.user_name.ilike(texto_like),
            models.Usuario.direccion.ilike(texto_like)
        )
    ).all()
    return resultados

'''# Eventos
def create_evento(db: Session, evento: schemas.EventoCreate):
    db_evento = models.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Evento).offset(skip).limit(limit).all()

def get_eventos_proximos(db: Session):
    ahora = datetime.utcnow()
    return db.query(models.Evento).filter(models.Evento.fecha_hora >= ahora).order_by(models.Evento.fecha_hora).all()
'''