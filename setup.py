# python libs
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# api lib
from api.comercio.models import Comercio
from api.processamento.models import Processamento
from api.exportacao.models import Exportacao
from api.importacao.models import Importacao
from api.producao.models import Producao
from api.config import settings
from api.database import Base

# data lib
from data import (
    comercio_pipeline,
    processamento_pipeline,
    exportacao_pipeline,
    importacao_pipeline,
    producao_pipeline
)

# const
from const import (
    comercio_url,
    processamento_urls,
    exportacao_urls,
    importacao_urls,
    producao_url
)

import logging

# logging configuration
logging.root = logging.getLogger('api')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)



async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # await asyncio.sleep(0.250)


def run_pipe(pipeline, url_path):
        return pipeline(url_path)

# Define async function for batch insertion into multiple tables
async def insert_data(session, data, table):
    async with session.begin():
        # Create the insert statement
        insert_stmt = table.__table__.insert().values(data)
        # Execute the insert statement
        await session.execute(insert_stmt)
    # await asyncio.sleep(0.250)



async def main():
    # 
    engine = create_async_engine(
        settings.DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=3600
    )

    SessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        future=True,
        class_=AsyncSession 
    )

    # create tables on db
    await create_tables(engine)

    logging.info('getting data')

    comercio = comercio_pipeline(comercio_url).to_dict(orient='records')
    processamento = processamento_pipeline(processamento_urls).to_dict(orient='records')
    exportacao = exportacao_pipeline(exportacao_urls).to_dict(orient='records')
    importacao = importacao_pipeline(importacao_urls).to_dict(orient='records')
    producao = producao_pipeline(producao_url).to_dict(orient='records')

    logging.info('data finish')

    async with SessionLocal() as session:
        logging.info('inside session local')
        await insert_data(session, comercio, Comercio)
        await insert_data(session, processamento, Processamento)
        await insert_data(session, exportacao, Exportacao)
        await insert_data(session, importacao, Importacao)
        await insert_data(session, producao, Producao)
    # await asyncio.sleep(0.250)

    logging.info('finish process')

    await engine.dispose()
    

if __name__ == '__main__':
# Run the main function synchronously
    asyncio.run(main())
