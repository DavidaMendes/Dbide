from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


class EmpresaRoutes:
    router = APIRouter(tags=["empresas"])

    @router.post("/empresas/", response_model=schemas.Empresa, status_code=201)
    async def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
        if db.query(models.Empresa).filter(models.Empresa.cnpj == empresa.cnpj).first():
            return JSONResponse({"message": "Empresa já cadastrada"}, 400)

        orm_empresa = models.Empresa(**empresa.model_dump())

        db.add(orm_empresa)
        db.commit()
        db.refresh(orm_empresa)

        return orm_empresa

    @router.get("/empresas/", response_model=list[schemas.Empresa])
    async def read_empresas(db: Session = Depends(get_db)):
        orm_empresas = db.query(models.Empresa).all()

        return orm_empresas

    @router.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
    async def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
        orm_empresa = db.get(models.Empresa, empresa_id)

        if orm_empresa is None:
            return JSONResponse({"message": "Empresa não encontrada"}, 404)

        return orm_empresa

    @router.put("/empresas/{empresa_id}", response_model=schemas.Empresa)
    async def update_empresa(
        empresa_id: int, empresa: schemas.EmpresaUpdate, db: Session = Depends(get_db)
    ):
        orm_empresa = db.get(models.Empresa, empresa_id)

        if orm_empresa is None:
            return JSONResponse({"message": "Empresa não encontrada"}, 404)

        for key, value in empresa.model_dump().items():
            setattr(orm_empresa, key, value)

        db.commit()
        db.refresh(orm_empresa)

        return orm_empresa

    @router.delete("/empresas/{empresa_id}", status_code=204)
    async def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
        orm_empresa = db.get(models.Empresa, empresa_id)

        if orm_empresa is None:
            return JSONResponse({"message": "Empresa não encontrada"}, 404)

        db.delete(orm_empresa)
        db.commit()


class ObrigacaoAcessoriaRoutes:
    router = APIRouter(tags=["obrigacoes"])

    @router.post("/obrigacoes/", response_model=schemas.ObrigacaoAcessoria, status_code=201)
    async def create_obrigacao(
        obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)
    ):
        if obrigacao.periodicidade not in ["mensal", "trimestral", "anual"]:
            return JSONResponse(
                {
                    "message": "O campo periodicidade deve ser uma das seguintes opções (mensal, trimestral, anual)"
                },
                400,
            )

        orm_empresa = db.get(models.Empresa, obrigacao.empresa_id)

        if orm_empresa is None:
            return JSONResponse(
                {"message": f"Empresa com id {obrigacao.empresa_id} não existe"}, 400
            )

        orm_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())

        db.add(orm_obrigacao)
        db.commit()
        db.refresh(orm_obrigacao)

        return orm_obrigacao

    @router.get("/obrigacoes/", response_model=list[schemas.ObrigacaoAcessoria])
    async def read_obrigacoes(db: Session = Depends(get_db)):
        orm_obrigacoes = db.query(models.ObrigacaoAcessoria).all()

        return orm_obrigacoes

    @router.get("/obrigacoes/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
    async def read_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
        orm_obrigacao = db.get(models.ObrigacaoAcessoria, obrigacao_id)

        if orm_obrigacao is None:
            return JSONResponse({"message": "Obrigação Acessória não encontrada"}, 404)

        return orm_obrigacao

    @router.put("/obrigacoes/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
    async def update_obrigacao(
        obrigacao_id: int,
        obrigacao: schemas.ObrigacaoAcessoriaUpdate,
        db: Session = Depends(get_db),
    ):
        orm_obrigacao = db.get(models.ObrigacaoAcessoria, obrigacao_id)

        if orm_obrigacao is None:
            return JSONResponse({"message": "Obrigação Acessória não encontrada"}, 404)

        if obrigacao.periodicidade not in ["mensal", "trimestral", "anual"]:
            return JSONResponse(
                {
                    "message": "O campo periodicidade deve ser uma das seguintes opções (mensal, trimestral, anual)"
                },
                400,
            )

        orm_empresa = db.get(models.Empresa, obrigacao.empresa_id)

        if orm_empresa is None:
            return JSONResponse(
                {"message": f"Empresa com id {obrigacao.empresa_id} não existe"}, 400
            )

        for key, value in obrigacao.model_dump().items():
            setattr(orm_obrigacao, key, value)

        db.commit()
        db.refresh(orm_obrigacao)

        return orm_obrigacao

    @router.delete("/obrigacoes/{obrigacao_id}", status_code=204)
    async def delete_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
        orm_obrigacao = db.get(models.ObrigacaoAcessoria, obrigacao_id)

        if orm_obrigacao is None:
            return JSONResponse({"message": "Obrigação Acessória não encontrada"}, 404)

        db.delete(orm_obrigacao)
        db.commit()
