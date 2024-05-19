import pandas as pd
import numpy as np
from pandas import DataFrame


def read_from_csv(path: str) -> DataFrame:
    """
    Function to read the .csv file from embrapa commerce values.
    Args:
        path (str): string path of file (can be an url as well).
    Returns:
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
        value_name='values'
    )


def sum_columns_with_same_year(data: DataFrame) -> DataFrame:
    """
    Sums the values of the dataframe columns that have the same year.
    Args:
        data (DataFrame): DataFrame with columns for years from 1970 to 2022.
    Returns:
        DataFrame: A pandas DataFrame with the year columns added together.
    """
    df = data
    df['quantity'] = np.where(df['year'].str.contains('.1'), df['values'], 1)
    df['valor R$'] = np.where(~df['year'].str.contains('.1'), df['values'], 0)
    df['year'] = df['year'].str.replace('.1', '')
    df = df.groupby(['País', 'year']).agg(
        {'quantity': 'sum', 'valor R$': 'sum'}
    ).reset_index()

    return df


def remove_rows_without_import_value(data: DataFrame) -> DataFrame:
    """
    Remove rows from the dataframe that have no trade value.
    Args:
        data (DataFrame): DataFrame with trading columns.
    Returns:
        DataFrame: A pandas DataFrame without rows with no import value.
    """
    filter = data['values'] > 0
    return data[filter]


# Função de teste detalhada
"""def run_tests():
    print("Running tests...")
    # Teste para read_from_csv
    df = read_from_csv('ExpVinho.csv')
    print("\nread_from_csv result:")
    print(df)
    if not df.empty:
        print("read_from_csv passed!")
    else:
        print("read_from_csv failed!")
    # Teste para unpivot_years_columns
    melted_df = unpivot_years_columns(df)
    print("\nunpivot_years_columns result:")
    print(melted_df)
    if not melted_df.empty:
        print("unpivot_years_columns passed!")
    else:
        print("unpivot_years_columns failed!")
    #Teste para sum_columns_with_same_year
    summed_df = sum_columns_with_same_year(melted_df)
    print("\nsum_columns_with_same_year result:")
    print(summed_df)
    if not summed_df.empty:
        print("sum_columns_with_same_year passed!")
    else:
        print("sum_columns_with_same_year failed!")
    # Teste para remove_rows_without_import_value
    filtered_df = remove_rows_without_import_value(melted_df)
    print("\nremove_rows_without_import_value result:")
    print(filtered_df)
    if not filtered_df.empty:
        print("remove_rows_without_import_value passed!")
    else:
        print("remove_rows_without_import_value failed!")
    print("All tests completed.")
if __name__ == "__main__":
    run_tests()
"""