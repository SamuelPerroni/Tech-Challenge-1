import pandas as pd
from data.Processamento import nodes


def processamento_pipeline(urls: list[str]) -> pd.DataFrame:
    dfs = []
    cont = 0

    for url in urls:
        df = nodes.read_from_csv(url)
        df = nodes.new_col_type(df)
        df = nodes.new_col_class(df, cont)
        df = nodes.drop_totals(df)
        df = nodes.unpivot_years_columns(df)
        df = nodes.remove_not_numbers(df)
        dfs.append(df)
        cont += 1

    return pd.concat(dfs)
