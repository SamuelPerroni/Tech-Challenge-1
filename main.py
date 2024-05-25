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

app.include_router(comercio_router, prefix="/comercio")
app.include_router(exportacao_router, prefix="/exportacao")
app.include_router(importacao_router, prefix="/importacao")
app.include_router(processamento_router, prefix="/processamento")
app.include_router(producao_router, prefix="/producao")
app.include_router(security_router, prefix="/jwt")


@app.get("/health", status_code=200)
async def root():
    return HTTPStatus.OK

#function to create the database when we create the API
# this fuction won't go to production env
async def startup_database_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# async def teardown_database_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

app.add_event_handler("startup", startup_database_event)
# app.add_event_handler("shutdown", teardown_database_event)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

