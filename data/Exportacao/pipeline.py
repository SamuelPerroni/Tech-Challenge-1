import pandas as pd
from data.Exportacao import nodes
from pandas import DataFrame
from typing import Dict


def exportacao_pipeline(import_datas: Dict[str, str]) -> DataFrame:
    df_comp = DataFrame()
    for nome, path in import_datas.items():
        df = nodes.read_from_csv(path=path)
        df = nodes.unpivot_years_columns(df)
        df = nodes.sum_columns_with_same_year(df)

        # Verificação se a coluna 'values' existe após a soma
        if 'values' not in df.columns:
            # Tentar encontrar a coluna que deveria ser 'values'
            if 'valor R$' in df.columns:
                df = df.rename(columns={'valor R$': 'values'})
            else:
                raise KeyError(f"The column 'values' was not found in the DataFrame after summing columns for {nome}.")

        df = nodes.remove_rows_without_import_value(df)
        df['Tipo'] = nome  # add type column with imported product name
        df_comp = pd.concat([df_comp, df], ignore_index=True)
    # Ordenar os dados pelo ano em ordem crescente
    df_comp = df_comp.sort_values(by='year').reset_index(drop=True)

    return df_comp
