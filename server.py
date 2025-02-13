from fastapi import FastAPI
from routes import router
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")