# from pytest import fixture
import pytest_asyncio
from api import Base, engine
from api.comercio.schemas import ComercioIn
from api.processamento.schemas import ProcessamentoIn
from api.importacao.schemas import ImportIn
from api.producao.schemas import ProducaoIn
from api.security.schemas import UserIn
from api.exportacao.schemas import ExportacaoIn



from faker import Faker

class ComercioFactory:
    @classmethod
    def generate_product(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def generate_year(cls):
        return int(Faker().year())
    
    @classmethod
    def generate_commerce(cls):
        return Faker().pyfloat(left_digits=4, positive=True, right_digits=2)
    
    @classmethod
    def generate_description_type(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def build(cls):
        return ComercioIn(
            product=Faker().pystr(min_chars=3, max_chars=16),
            year=int(Faker().year()),
            commerce=Faker().pyfloat(left_digits=4, positive=True, right_digits=2),
            description_type=Faker().pystr(min_chars=3, max_chars=16)
        )


@pytest_asyncio.fixture
async def create_and_drop_db_yield_engine():
    # set up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    # tear down
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def create_test_client():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    return client


@pytest_asyncio.fixture
async def create_fake_data():
    
    return ComercioFactory().build


@pytest_asyncio.fixture
async def run_pipeline():
    from data.Comercio.pipeline import comercio_pipeline
    from const import comercio_url
    data = comercio_pipeline(comercio_url)
    return data.head(5)


###### Config processamento test
################################
################################
################################
################################
################################
################################

class ProcessamentoFactory:
    @classmethod
    def generate_product_type(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def generate_full_product_name(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def generate_classification(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def generate_year(cls):
        return int(Faker().year())
    
    @classmethod
    def generate_commerce(cls):
        return Faker().pyint(min_value=10, max_value= 10000)
    
    
    @classmethod
    def build(cls):
        return ProcessamentoIn(
            product_type=Faker().pystr(min_chars=3, max_chars=16),
            full_product_name=Faker().pystr(min_chars=3, max_chars=16),
            classification=Faker().pystr(min_chars=3, max_chars=16),
            year=int(Faker().year()),
            commerce=Faker().pyint(min_value=10, max_value= 10000)
        )
    
@pytest_asyncio.fixture
async def create_fake_data_processamento():
    
    return ProcessamentoFactory().build

@pytest_asyncio.fixture
async def run_pipeline_processamento():
    from data.Processamento.pipeline import processamento_pipeline
    from const import processamento_urls
    data = processamento_pipeline(processamento_urls)
    return data.head(5)


###### Config importacao test
################################
################################
################################
################################
################################
################################


class ImportacaoFactory:
    @classmethod
    def pais(cls):
        return Faker().pystr(min_chars=3, max_chars=16)


    @classmethod
    def year(cls):
        return Faker().pyint(min_value=10, max_value= 10000)


    @classmethod
    def quantity(cls):
        return Faker().pyfloat(left_digits=4, positive=True, right_digits=2)


    @classmethod
    def valor(cls):
        return Faker().pyfloat(left_digits=4, positive=True, right_digits=2)


    @classmethod
    def type(cls):
        return Faker().pystr(min_chars=3, max_chars=16)

 
    @classmethod
    def build(cls):
        return ImportIn(
            pais=Faker().pystr(min_chars=3, max_chars=16),
            year=Faker().pyint(min_value=10, max_value= 10000),
            quantity=Faker().pyfloat(left_digits=4, positive=True, right_digits=2),
            valor=Faker().pyfloat(left_digits=4, positive=True, right_digits=2),
            type=Faker().pystr(min_chars=3, max_chars=16)
        )
    
@pytest_asyncio.fixture
async def create_fake_data_importacao():
    
    return ImportacaoFactory().build

@pytest_asyncio.fixture
async def run_pipeline_importacao():
    from data.Importacao.pipeline import importacao_pipeline
    from const import importacao_urls
    data = importacao_pipeline(importacao_urls)
    return data.head(5)


###### Config JWT test
################################
################################
################################
################################
################################
################################

class UserFactory:
    @classmethod
    def generate_user_name(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def generate_user_pass(cls):
        return Faker().pystr(min_chars=3, max_chars=16)
    
    @classmethod
    def build(cls):
        return UserIn(
            user_name=Faker().pystr(min_chars=3, max_chars=16),
            user_pass=Faker().pystr(min_chars=3, max_chars=16),
        )
    
@pytest_asyncio.fixture
async def create_fake_data_user():
    
    return UserFactory().build


###### Config exportacao test
################################
################################
################################
################################
################################
################################

class ExportacaoFactory:    
    @classmethod
    def build(cls):
        return ExportacaoIn(
            pais=Faker().pystr(min_chars=3, max_chars=16),
            year=int(Faker().year()),
            quantity=Faker().pyint(),
            valor=Faker().pyfloat(left_digits=4, positive=True, right_digits=2),
            type=Faker().pystr(min_chars=3, max_chars=16)
        )
    
@pytest_asyncio.fixture
async def create_fake_data_exportacao():
    
    return ExportacaoFactory().build


@pytest_asyncio.fixture
async def run_pipeline_exportacao():
    from data.Exportacao.pipeline import exportacao_pipeline
    from const import exportacao_urls
    data = exportacao_pipeline(exportacao_urls)
    return data.head(5)


@pytest_asyncio.fixture
async def jwt_token_fixture(create_test_client,  create_fake_data_user):
    test_client = create_test_client
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}
    return header

###### Config producao test
################################
################################
################################
################################
################################
################################

class ProducaoFactory:    
    @classmethod
    def build(cls):
        return ProducaoIn(
            type=Faker().pystr(min_chars=3, max_chars=16),
            full_product_name=Faker().pystr(min_chars=3, max_chars=16),
            year=int(Faker().year()),
            value=Faker().pyint(min_value=10, max_value= 1000000000)
        )
    
@pytest_asyncio.fixture
async def create_fake_data_producao():
    
    return ProducaoFactory().build


@pytest_asyncio.fixture
async def run_pipeline_producao():
    from data.Producao.pipeline import producao_pipeline
    from const import producao_url
    return producao_pipeline(producao_url).head(5)
