from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate

from . import models, schemas, crud, database

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Atletas", version="1.0")

@app.post("/atletas/", response_model=schemas.AtletaOut, summary="Cria um novo atleta")
def criar_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(database.get_db)):
    """
    Cria um atleta no banco de dados.
    Retorna erro 303 se CPF já estiver cadastrado.
    """
    return crud.create_atleta(db, atleta)

@app.get("/atletas/", response_model=Page[schemas.AtletaOut], summary="Lista atletas com filtros e paginação")
def listar_atletas(
    db: Session = Depends(database.get_db),
    nome: str | None = Query(None, description="Filtrar atletas pelo nome"),
    cpf: str | None = Query(None, description="Filtrar atletas pelo CPF")
):
    """
    Retorna todos os atletas.
    Suporta filtros por nome e cpf, e paginação via fastapi-pagination.
    """
    atletas = crud.get_atletas(db, nome=nome, cpf=cpf)
    return paginate(atletas)

# Adiciona suporte à paginação
add_pagination(app)
