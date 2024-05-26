import pandas as pd
import numpy as np


def read_from_csv(path: str) -> pd.DataFrame:
    """
    Function to read the .csv file from producao commerce values.

    Args:
        path (str): string path of file (can be an url as well).

    Returnes:
        pd.DataFrame: A pandas dataframe of producao commerce values.
    """
    return pd.read_csv(path,
                       delimiter=';',
                       on_bad_lines='skip').rename(columns={
                           'control': 'produto',
                           'produto': 'full_product_name'
                       }).drop(['id'],axis=1)


def product_type(value: str) -> str:
    """
    Function to define product type

    Args:
        name (str): string of product name. (In the column 'produto')

    Returnes:
        str: string of type name
    """
    prefix = value[0:2]
    if prefix == 'vm':
        return 'VINHO DE MESA'
    elif prefix == 'vv':
        return 'VINHO FINO DE MESA(VINIFERA)'
    elif prefix == 'su':
        return 'SUCO'
    elif prefix == 'de':
        return 'DERIVADOS'
    else:
        return 'agregacao'


def new_col_type(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create a new column called 'type', drop "produto" and fix types

    Args:
        data (DataFrame): Dataframe that we want append a new column

    Returnes:
        pd.DataFrame: Dataframe after appending new column
    """
    new_column = data['produto'].apply(product_type)
    data.insert(loc=0, column='type', value=new_column)
    df_retorno = data[data['type'] != 'agregacao']
    df_retorno = df_retorno.drop(columns={'produto'})
    df_retorno['type'] = df_retorno['type'].astype(str)
    df_retorno['full_product_name'] = df_retorno['full_product_name'].astype(str)
    df_retorno['year'] =  df_retorno['year'].astype(int)
 
    
    return df_retorno



def unpivot_years_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Unpivot all year column into only one column named year.
    Also known as melt transformation.

    Args:
        data (pd.DataFrame): DataFrame with all column names from 1970 to 2022.

    Returns:
        pd.DataFrame: Pandas DataFrame with melted year columns.
    """
    return data.melt(id_vars=['produto','full_product_name'],
                     value_vars= None,
                     var_name='year',
                     value_name='value')
