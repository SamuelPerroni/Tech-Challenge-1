import psycopg2
import pandas as pd
from sqlalchemy.orm import Session

import database
from data import producao_pipeline
from database import Produto

from sqlalchemy import create_engine

from fastapi import FastAPI
import requests

app = FastAPI()

connection: psycopg2.extensions.connection


@app.get("/")
def read_root():
    return {"Hello": "ML1"}

@app.post("/products")
def create_produto(produto: Produto):
    session = Session(database.engine)
    session.add(produto)
    session.commit()
    return produto

@app.get("/products/{product_id}")
def read_produto(produto_id: int):
    session = Session(database.engine)
    record = session.query(Produto).filter(database.Product.id == produto_id).first()
    return record

@app.get("/production")
def read_all():
    session = Session(database.engine)
    records = session.query(Produto).all()
    return records


@app.get("/produtos/type/{produto_type}")
def read_producao_by_master(produto_type):
    session = Session(database.engine)
    records = session.query(database.Produto).filter(database.Produto.produto_type == produto_type).all()
    return records

@app.get("/produtos/master2/{produto_type}")
def read_produtos_by_master2(produto_type):
    session = Session(database.engine)
    records = session.query(database.Produto).filter(database.Produto.produto_type == produto_type).all()
    for record in records:
        print(record)
    return records

@app.detete("/produtos/{produto_id}")
def delete_produto(produto_id: int):
    session = Session(database.engine)
    session.query(database.Product).filter(database.Product.id == produto_id).delete()
    session.commit()
    return {"status": "ok"}

@app.patch("/produtos/{produto_id}")
def update_produto(produto_id: int, produto: Produto):
    session = Session(database.engine)
    session.query(database.Product).filter(database.Product.id == produto_id).update(produto)
    session.commit()
    return {"status": "ok"}




@app.get("/start-pipeline")
def start_pipeline():
    download_file('http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', 'Producao.csv')
    producao_pipeline('Producao.csv')
    return {"status": "ok"}


def insert_data_to_db(df, table_name, connection):
    # Create SQLAlchemy engine
    engine = create_engine(connection)

    # Insert the dataframe into the database in one go
    df.to_sql(table_name, engine, if_exists='append', index=False)

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    producao_pipeline('C:\\Users\\luizp\\Downloads\\Producao.csv')