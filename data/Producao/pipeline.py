from pandas import DataFrame
from data.Producao import nodes


def producao_pipeline(path: str) -> DataFrame:
    df = nodes.read_from_csv(path)
    df = nodes.drop_id(df)
    df = nodes.new_col_type(df)
    #df = nodes.drop_totals(df)
    df = nodes.unpivot_years_columns(df)
    df = nodes.save_to_db(df)
    return df
