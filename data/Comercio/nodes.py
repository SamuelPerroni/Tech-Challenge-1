import pandas as pd


def read_from_csv(path: str) -> pd.DataFrame:
    """
    Function to read the .csv file from embrapa commerce values.

    Args:
        path (str): string path of file (can be an url as well).

    Returnes:
        pd.DataFrame: A pandas dataframe of embrapa commerce values.
    """
    return pd.read_csv(path,
                       delimiter=';',
                       on_bad_lines='skip',
                       encoding='utf-8'
                       ).rename(columns={
                           'control': 'produto',
                           'Produto': 'full_product_name'
                       }).drop(['id'],axis=1)


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
                   id_vars=['produto', 'full_product_name'],
                   value_vars=None,
                   var_name='year',
                   value_name='commerce')


def split_type_and_product_and_drop_general_type(
        data: pd.DataFrame) -> pd.DataFrame:
    """
    Split type and name defined on product column. Ex: 'vm_Tinto' turns to:
        - type: 'vm'
        - producto: 'Tinto'

    Args:
        data (pd.DataFrame): Pandas DataFrame of melted yeaar columns.

    Returns:
        pd.DataFrame: new column type and produto
    """
    data[['type', 'produto']] = data['produto'].str.split('_',
                                                          n=1,
                                                          expand=True)
    return data


def rewrite_type_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    using foward fill to map values type to description type values.

    Args:
        data (pd.DataFrame): pandas DataFrame

    Returns:
        pd.DataFrame: description type definition.
    """
    mask = data['type'].str.isupper()
    data['description type'] = data.where(mask)['type']
    data['description type'] = data['description type'].ffill()
    return data


def drop_rows_totals(data):
    return data.dropna(subset='produto')


def select_columns(data):
    return data.loc[:, ['full_product_name', 'year', 'commerce', 'description type']].rename(
        columns={'full_product_name': 'product',
                 'description type': 'description_type'}
    )

def clean(data):
    data['product'] = data['product'].str.strip()
    return data