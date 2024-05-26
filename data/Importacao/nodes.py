import pandas as pd
import numpy as np
from pandas import DataFrame


def read_from_csv(path: str) -> DataFrame:
    """
    Function to read the .csv file from embrapa commerce values.

    Args:
        path (str): string path of file (can be an url as well).

    Returnes:
        DataFrame: A pandas dataframe of embrapa commerce values.
    """
    return pd.read_csv(
        path,
        delimiter=';',
        on_bad_lines='skip',
        encoding = 'utf8'
        )

def unpivot_years_columns(data: DataFrame) -> DataFrame:
    """
    Unpivot all year column into only one column named year.
    Also known as melt transformation.

    Args:
        data (DataFrame): DataFrame with all column names from 1970 to 2022.

    Returns:
        DataFrame: A pandas DataFrame with melted year columns.
    """
    return pd.melt(
        data,
        id_vars=['Id', 'País'],
        value_vars=None,
        var_name='year',
        value_name='values'
        )

def sum_collumns_with_same_year(data: DataFrame) -> DataFrame:
    """
    Sums the values of the dataframe columns that have the same year.

    Args:
        data (DataFrame): DataFrame with columns for years from 1970 to 2022.

    Returns:
        DataFrame: A pandas DataFrame with the year columns added together.
    """
    df = data
    df['quantity'] = np.where(~df['year'].str.contains('.1', regex=False), df['values'], 0.0)
    df['valor R$'] = np.where(df['year'].str.contains('.1',  regex=False), df['values'], 0.0)
    df['year'] = df['year'].str.replace('.1', '')
    return df.groupby(['País',  'year'], as_index=False).agg({'quantity': 'sum', 'valor R$': 'sum'})

