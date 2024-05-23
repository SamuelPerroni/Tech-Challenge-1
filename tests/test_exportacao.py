from api import engine
import pytest

from data import exportacao_pipeline
from data.Exportacao.nodes import read_from_csv, unpivot_years_columns, sum_columns_with_same_year, \
    remove_rows_without_import_value


# Função de teste detalhada
def run_tests():
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


# Função de teste detalhada
def run_tests():
    print("Running tests...")
    # Teste para read_from_csv
    df = read_from_csv('ExpVinho.csv')
    print("\nread_from_csv result:")
    print(df)
    if not df.empty:
        print("read_from_csv passed!")
    else:
        print("read_from_csv failed!")
    # Teste para unpivot_years_columns
    melted_df = unpivot_years_columns(df)
    print("\nunpivot_years_columns result:")
    print(melted_df)
    if not melted_df.empty:
        print("unpivot_years_columns passed!")
    else:
        print("unpivot_years_columns failed!")
    #Teste para sum_columns_with_same_year
    summed_df = sum_columns_with_same_year(melted_df)
    print("\nsum_columns_with_same_year result:")
    print(summed_df)
    if not summed_df.empty:
        print("sum_columns_with_same_year passed!")
    else:
        print("sum_columns_with_same_year failed!")
    # Teste para remove_rows_without_import_value
    filtered_df = remove_rows_without_import_value(melted_df)
    print("\nremove_rows_without_import_value result:")
    print(filtered_df)
    if not filtered_df.empty:
        print("remove_rows_without_import_value passed!")
    else:
        print("remove_rows_without_import_value failed!")
    print("All tests completed.")

if __name__ == "__main__":
    run_tests()
