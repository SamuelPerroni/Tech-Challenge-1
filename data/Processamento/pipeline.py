from pandas import DataFrame
from data.Processamento import nodes


def processamento_pipeline(path: str) -> DataFrame:
    df = nodes.read_from_csv(path)
    df = nodes.new_col_type(df)
    df = nodes.drop_totals(df)
    df = nodes.remove_notNumbers(df)
    df = nodes.unpivot_years_columns(df)
    return df
