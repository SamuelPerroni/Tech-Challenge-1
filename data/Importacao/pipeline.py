import pandas as pd
from pandas import DataFrame
from typing import Dict

from data.Importacao import nodes


def importacao_pipeline(import_datas: Dict[str, str]) -> DataFrame:
    df_comp = DataFrame() 
    for nome, path in import_datas.items():
        df = nodes.read_from_csv(path=path)
        df = nodes.unpivot_years_columns(df)
        df = nodes.sum_collumns_with_same_year(df)
        df['type'] = nome # add type column with imported product name
        df_comp = pd.concat([df_comp, df])
    
    df_comp = df_comp.rename(columns={"País": "pais", "valor R$" : "valor"})
    return df_comp
