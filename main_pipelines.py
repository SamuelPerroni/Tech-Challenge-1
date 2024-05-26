from data import producao_pipeline
from data import processamento_pipeline
from const import producao_url
from const import processamento_urls

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine

from api.config import settings

if __name__ == '__main__':


    data = producao_pipeline(producao_url).head(2)
    print(data.info())
