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


@app.get("/producao")
def read_all():
    session = Session(database.engine)
    records = session.query(Produto).all()
    return records


@app.get("/produtos/master/{produto_master}")
def read_producao_by_master(produto_master):
    session = Session(database.engine)
    records = session.query(database.Produto).filter(database.Produto.produto_master == produto_master).all()
    return records

@app.get("/produtos/master2/{produto_master}")
def read_produtos_by_master2(produto_master):
    session = Session(database.engine)
    records = session.query(database.Produto).filter(database.Produto.produto_master == produto_master).all()
    for record in records:
        print(record)
    return records


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