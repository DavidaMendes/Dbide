from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import EmpresaRoutes, ObrigacaoAcessoriaRoutes

app = FastAPI()

app.include_router(EmpresaRoutes.router)
app.include_router(ObrigacaoAcessoriaRoutes.router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
