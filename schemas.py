from pydantic import BaseModel


class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefonde: str


class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_model = True


class EmpresaCreate(EmpresaBase):
    pass


class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: str


class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int

    class Config:
        orm_model = True


class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass 