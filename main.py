from fastapi import FastAPI
from http import HTTPStatus
import uvicorn

from api.comercio.routes import comercio_router
from api.exportacao.routes import exportacao_router
from api.importacao.routes import importacao_router
from api.processamento.routes import processamento_router
from api.producao.routes import producao_router

from api.database import Base

app = FastAPI()

app.include_router(comercio_router, prefix="/comercio")
app.include_router(exportacao_router, prefix="/exportacao")
app.include_router(importacao_router, prefix="/importacao")
app.include_router(processamento_router, prefix="/processamento")
app.include_router(producao_router, prefix="/producao")


@app.get("/health", status_code=200)
async def root():
    return HTTPStatus.OK


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)