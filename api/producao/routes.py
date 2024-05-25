import requests
from fastapi import APIRouter, HTTPException, status

from api import SessionLocal, database
from api.producao.models import Product
from data import producao_pipeline

# rotas de exportacao
app = APIRouter()

@app.get("/")
async def root():
    return {"message": "Hello producao_router"}

@app.get("/")
def read_root():
    return {"Hello": "ML1"}

@app.post("/products")
def create_product(product: Product):
    session = SessionLocal()
    session.add(product)
    session.commit()
    return product

@app.get("/products/{product_id}")
def read_product(Product_id: int):
    session = SessionLocal()
    record = session.query(Product).filter(database.Product.id == Product_id).first()
    return record

@app.get("/production")
def read_all():
    session = SessionLocal()
    records = session.query(Product).all()
    return records

@app.get("/Products/type/{Product_type}")
def read_producao_by_master(Product_type):
    session = SessionLocal()
    records = session.query(database.Product).filter(database.Product.Product_type == Product_type).all()
    return records

@app.get("/Products/master2/{Product_type}")
def read_products_by_master2(Product_type):
    session = SessionLocal()
    records = session.query(database.Product).filter(database.Product.Product_type == Product_type).all()
    for record in records:
        print(record)
    return records

@app.detete("/Products/{Product_id}")
def delete_product(Product_id: int):
    session = SessionLocal()
    session.query(database.Product).filter(database.Product.id == Product_id).delete()
    session.commit()
    return {"status": "ok"}

@app.patch("/Products/{Product_id}")
def update_product(Product_id: int, Product: Product):
    session = SessionLocal()
    session.query(database.Product).filter(database.Product.id == Product_id).update(Product)
    session.commit()
    return {"status": "ok"}

@app.get("/start-pipeline")
def start_pipeline():
    download_file('http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', 'Producao.csv')
    producao_pipeline('Producao.csv')
    return {"status": "ok"}


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)