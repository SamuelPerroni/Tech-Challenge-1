import pandas as pd
from pandas import DataFrame
from data.Importacao import nodes
from typing import List


def importacao_pipeline(paths: List[str]) -> DataFrame:
    df_comp = DataFrame() 
    for path in paths:
        df = nodes.read_from_csv(path=path)
        df = nodes.sum_collumns_same_year(df)
        df = nodes.unpivot_years_columns(df)
        df = nodes.remove_rows_without_import_value(df)
        df = df.drop('Id', axis=1)
        df_comp = pd.concat([df])
        
    return df_comp
