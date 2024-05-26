from data import producao_pipeline
from data import processamento_pipeline
from data import comercio_pipeline
from const import producao_url
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
  data = comercio_pipeline(comercio_url).head(2)
  print(data.to_dict('records'))
  print(data)



