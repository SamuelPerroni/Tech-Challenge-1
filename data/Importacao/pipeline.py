from pandas import DataFrame
from data.Importacao import nodes
from typing import List


def importacao_pipeline(paths: List[str]) -> List[DataFrame]:
    df_list: List[DataFrame] = []
    for path in paths:
        df = nodes.read_from_csv(path=path)
        df = nodes.sum_collumns_same_year(df)
        df = nodes.unpivot_years_columns(df)
        df = df.drop('Id', axis=1)
        df_list.append(df)
        
        return df_list
