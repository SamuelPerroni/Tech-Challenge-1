import pandas as pd
import numpy as np

import database

def read_from_csv(path: str) -> pd.DataFrame:
    """
    Function to read the .csv file from producao commerce values.

    Args:
        path (str): string path of file (can be an url as well).

    Returnes:
        pd.DataFrame: A pandas dataframe of producao commerce values.
    """
    df = pd.read_csv(path, delimiter=';')
    name_list = ['id', 'produto'] + list(range(1970, 2023, 1))
    return pd.read_csv(path,
                       delimiter=';',
                       header=1,
                       names=name_list,
                       on_bad_lines='skip')


def product_type(value: str) -> str:
    """
    Function to define product type

    Args:
        name (str): string of product name. (In the column 'produto')

    Returnes:
        str: string of type name
    """
    if value.isupper():
        return value
    else:
        return ''


def new_col_type(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a new column called 'type'

    Args:
        data (DataFrame): Dataframe that we want append a new column

    Returnes:
        pd.DataFrame: Dataframe after appending new column
    """
    new_column = data['produto'].apply(product_type)
    data.insert(loc=0, column='product_type', value=new_column)
    return data

def drop_id(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to drop aggregation lines

    Args:
        data (DataFrame): Dataframe that we want drop totals

    Returnes:
        pd.DataFrame: Dataframe after drop
    """
    data = data.drop(columns=['id'])
    return data


def drop_totals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to drop aggregation lines

    Args:
        data (DataFrame): Dataframe that we want drop totals

    Returnes:
        pd.DataFrame: Dataframe after drop
    """
    data = data[data['product_type'] != '']
    return data


def unpivot_years_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Unpivot all year column into only one column named year.
    Also known as melt transformation.

    Args:
        data (pd.DataFrame): DataFrame with all column names from 1970 to 2022.

    Returns:
        pd.DataFrame: Pandas DataFrame with melted year columns.
    """
    return data.melt(id_vars=['product_type', 'product'],
                   var_name='year',
                   value_name='value')


def remove_not_numbers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to change not number values to NaN

    Args:
        data (DataFrame): Dataframe that we want change not numbers values

    Returnes:
        pd.DataFrame: Dataframe after the changes
    """

    return data.map(lambda x: np.nan if (x == '*' or x == 'nd') else x)

def save_to_db(df: pd.DataFrame):
    connection = connect_to_db()
    session = database.SessionLocal
    produto_type = ''
    index: int = 0
    for index, row in df.iterrows():
        if row['produto'].isupper():
            produto_type = row['produto']
        else:
            index += 1
            new_produto = Produto(id=index, produto_type=produto_type, produto=row['produto'], year=row['year'], production=row['value'])
            session.add(new_produto)
            session.commit()

    # Print the transformed dataframe
    print(df)
    # Read the CSV file
    session.close()

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