from fastapi import FastAPI
from http import HTTPStatus
from api.database import engine
import uvicorn

from api.comercio.routes import comercio_router
from api.exportacao.routes import exportacao_router
from api.importacao.routes import importacao_router
from api.processamento.routes import processamento_router
from api.producao.routes import producao_router
from api.security.routes import security_router
from api.database import Base

app = FastAPI()

app.include_router(security_router, prefix="/security", tags=['security'])
app.include_router(comercio_router, prefix="/comercio", tags=["comercio"])
app.include_router(exportacao_router, prefix="/exportacao", tags=['exportacao'])
app.include_router(importacao_router, prefix="/importacao", tags=['importacao'])
app.include_router(processamento_router, prefix="/processamento", tags=['processamento'])
app.include_router(producao_router, prefix="/producao", tags=['producao'])

@app.get("/health", status_code=200)
async def root():
    return HTTPStatus.OK


if __name__ == '__main__':
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=8000)

