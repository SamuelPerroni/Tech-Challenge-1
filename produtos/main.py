import psycopg2
import pandas as pd
from sqlalchemy.orm import session, Session

import database
from database import Produto

from sqlalchemy import create_engine, select

from fastapi import FastAPI

app = FastAPI()

connection: psycopg2.extensions.connection


@app.get("/")
def read_root():
    return {"Hello": "ML1"}


@app.get("/produtos")
def read_all():
    session = Session(database.engine)
    records = session.query(Produto).all()
    return records


@app.get("/produtos/master/{produto_master}")
def read_produtos_by_master(produto_master):
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


@app.get("/carga")
def carga():
    collect_data('C:\\Users\\luizp\\Downloads\\Producao.csv')
    return {"status": "ok"}


def insert_data_to_db(df, table_name, connection):
    # Create SQLAlchemy engine
    engine = create_engine(connection)

    # Insert the dataframe into the database in one go
    df.to_sql(table_name, engine, if_exists='append', index=False)


def collect_data(file_name):
    # Read the CSV file
    df = pd.read_csv(file_name, delimiter=';')

    # Melt the dataframe
    df_melted = df.melt(id_vars=['id', 'produto'], var_name='year', value_name='value')

    connection = connect_to_db()
    produto_master = ''
    index: int = 0
    for index, row in df_melted.iterrows():
        if row['produto'].isupper():
            produto_master = row['produto']
        else:
            index += 1
            connection.cursor().execute(
                f"INSERT INTO produtos (id, produto_master, produto, ano, valor) VALUES ('{index}','{produto_master}','{row['produto']}', '{row['year']}', '{row['value']}')")
    connection.commit()
    connection.close()
    # Print the transformed dataframe
    print(df_melted)
    # Read the CSV file


def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="changeme",
            host="localhost",
            port="5432",
            database="dbml1"
        )

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if (connection):
            cursor.close()
            # connection.close()
            # print("PostgreSQL connection is closed")
    return connection
