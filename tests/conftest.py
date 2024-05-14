# from pytest import fixture
import pytest_asyncio
from api import Base, engine
from api.comercio.schemas import ComercioIn


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