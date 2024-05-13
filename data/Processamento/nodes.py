import pandas as pd
import numpy as np


def read_from_csv(path: str) -> pd.DataFrame:
    """
    Function to read the .csv file from embrapa commerce values.

    Args:
        path (str): string path of file (can be an url as well).

    Returnes:
        pd.DataFrame: A pandas dataframe of embrapa commerce values.
    """
    name_list = ['produto', 'full_product_name'] + list(range(1970, 2023, 1))
    return pd.read_csv(path,
                       delimiter='\t',
                       header=0,
                       names=name_list,
                       on_bad_lines='skip')


def product_type(name: str) -> str:
    """
    Function to define product type

    Args:
        name (str): string of product name. (In the column 'produto')

    Returnes:
        str: string of type name
    """
    prefix = name[0:2]
    if prefix == 'ti':
        return 'TINTAS'
    elif prefix == 'br':
        return 'BRANCAS_ROSADAS'
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
    return pd.melt(data,
                   id_vars=['product_type',
                            'produto',
                            'full_product_name',
                            'classification'],
                   value_vars=None,
                   var_name='year',
                   value_name='commerce')


def remove_not_numbers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to drop not number values

    Args:
        data (DataFrame): Dataframe that we want change not numbers values

    Returnes:
        pd.DataFrame: Dataframe after the changes
    """

    indexs = data[data['commerce'].isin(["*", "nd"])].index
    return data.drop(indexs)


def new_col_class(data: pd.DataFrame, classification: int) -> pd.DataFrame:
    """
    Function to create a new column called 'classification'

    Args:
        data (DataFrame): Dataframe that we want append a new column

    Returnes:
        pd.DataFrame: Dataframe after appending new column
    """

    new_col = ''

    if classification == 0:
        new_col = 'viniferas'
    elif classification == 1:
        new_col = 'americanas_hibridas'
    elif classification == 2:
        new_col = 'uvas_mesa'
    else:
        new_col = 'sem_classificacao'

    data['classification'] = new_col
    return (data)
