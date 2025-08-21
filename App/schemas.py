from pydantic import BaseModel

class AtletaCreate(BaseModel):
    """Schema para criação de atleta."""
    nome: str
    cpf: str
    centro_treinamento: str | None = None
    categoria: str | None = None

class AtletaOut(BaseModel):
    """Schema de saída de atleta."""
    nome: str
    centro_treinamento: str | None
    categoria: str | None

    class Config:
        orm_mode = True
