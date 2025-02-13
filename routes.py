from fastapi import APIRouter, Depends, HTTPException
import schemas, models
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/empresas/", response_model=schemas.Empresa)
def create_empresa(empresa:schemas.EmpresaCreate, db:Session=Depends(get_db)):
    orm_empresa = models.Empresa(**empresa.model_dump())

    db.add(orm_empresa)
    db.commit()
    db.refresh(orm_empresa)

    return orm_empresa
    