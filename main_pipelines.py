from data import comercio_pipeline
from data import processamento_pipeline
from data import exportacao_pipeline
from const import comercio_url
from const import exportacao_urls
from const import processamento_urls

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine

from api.config import settings

if __name__ == '__main__':



    for x in processamento_urls:
        print(processamento_pipeline(x).info())

    for x in exportacao_urls:
        print(exportacao_pipeline(x).info())

    data = processamento_pipeline(processamento_urls).head(2)
    print(data.to_dict('records'))
    print(data.info())

    print(comercio_pipeline(comercio_url).head(5))

