from pandas import DataFrame
from data.Comercio import nodes


def comercio_pipeline(path: str) -> DataFrame:
    df = nodes.read_from_csv(path=path)
    df = nodes.unpivot_years_columns(df)
    df = nodes.split_type_and_product_and_drop_general_type(df)
    df = nodes.rewrite_type_names(df)
    df = nodes.drop_rows_totals(df)
    df = nodes.select_columns(df)
    
    return df
