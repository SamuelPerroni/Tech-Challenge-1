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
        df = nodes.remove_rows_without_import_value(df)
        df['Tipo'] = nome  # add type column with imported product name
        df_comp = pd.concat([df_comp, df], ignore_index=True)

    # Ordenar os dados pelo ano em ordem crescente
    df_comp = df_comp.sort_values(by='year').reset_index(drop=True)

    return df_comp


# Função de teste detalhada
"""def run_tests():
    print("Running tests...")

    import_datas = {
        'Vinhos de mesa': 'ExpVinho.csv',
        'Espumantes': 'ExpEspumantes.csv',
        'Uvas frescas': 'ExpUva.csv',
        'Suco de uva': 'ExpSuco.csv'
    }

    result_df = exportacao_pipeline(import_datas)
    print("\nFinal result from exportacao_pipeline:")
    print(result_df)
    if not result_df.empty:
        print("exportacao_pipeline passed!")
    else:
        print("exportacao_pipeline failed!")

    print("All tests completed.")


if __name__ == "__main__":
    run_tests()
"""
