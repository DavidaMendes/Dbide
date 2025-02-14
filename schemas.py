from pydantic import BaseModel


class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str


class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_model = True


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nome: str
    endereco: str
    email: str
    telefone: str


class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int


class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int

    class Config:
        orm_model = True


class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass


class ObrigacaoAcessoriaUpdate(ObrigacaoAcessoriaBase):
    pass
