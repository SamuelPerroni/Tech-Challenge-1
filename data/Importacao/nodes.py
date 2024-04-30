import pandas as pd
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
        on_bad_lines='skip'
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
        value_name='commerce'
        )


def sum_collumns_same_year(data: DataFrame) -> DataFrame:
    """
    Sums the values of the dataframe columns that have the same year.

    Args:
        data (DataFrame): DataFrame with columns for years from 1970 to 2022.

    Returns:
        DataFrame: A pandas DataFrame with the year columns added together.
    """
    df = data
    years = list(range(1970, 2023, 1))

    for year in years:
        string_year = str(year)
        df[string_year] = df[string_year] + df[f'{string_year}.1']
        df = df.drop(f'{string_year}.1', axis=1)
        
    return df

def remove_rows_without_commerce_value(data: DataFrame) -> DataFrame:
    """
    Remove rows from the dataframe that have no trade value.

    Args:
        data (DataFrame): DataFrame with trading columns.

    Returns:
        DataFrame: A pandas DataFrame without rows with no import value.
    """
    filter = data['commerce'] > 0
  
    return data[filter]
