from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

def create_atleta(db: Session, atleta: schemas.AtletaCreate):
    """
    Cria um novo atleta no banco.
    Lança HTTPException 303 se o CPF já existir.
    """
    db_atleta = models.Atleta(**atleta.dict())
    db.add(db_atleta)
    try:
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )

def get_atletas(db: Session, skip: int = 0, limit: int = 10, nome: str | None = None, cpf: str | None = None):
    """
    Retorna lista de atletas com filtros opcionais por nome e cpf.
    Suporta paginação via skip e limit.
    """
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return query.offset(skip).limit(limit).all()
