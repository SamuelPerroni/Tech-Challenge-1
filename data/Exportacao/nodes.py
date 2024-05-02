import pandas as pd


def read_from_csv(path: str) -> pd.DataFrame:
    """
    Função para ler o arquivo CSV com os dados de exportação.

    Args:
        path (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame pandas com os dados de exportação.
    """
    # Lendo o arquivo CSV com o formato fornecido
    df = pd.read_csv(path, delimiter=';', encoding='utf-8')

    return df


def process_export_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processa os dados de exportação para obter o formato desejado.

    Args:
        data (pd.DataFrame): DataFrame com os dados de exportação.

    Returns:
        pd.DataFrame: DataFrame pandas com os dados processados.
    """
    processed_data = []
    for _, row in data.iterrows():
        id_value = row.get('Id')
        country = row.get('País')
        row_data = {'Id': id_value, 'País': country}
        for i in range(2, len(row), 2):  # Começa na col 3 e increme 2 em 2
            year = row.index[i].split('-')[0]  # Obtém o ano da coluna
            quantity = row.iloc[i]  # Obtém a quantidade usando iloc
            value = row.iloc[i + 1]  # Obtém o valor usando iloc
            row_data[f"{year}-Quantidade"] = quantity
            row_data[f"{year}-Valor"] = value
        processed_data.append(row_data)

    return pd.DataFrame(processed_data)



# Escolha o caminho para o arquivo CSV

"""caminho_arquivo = "ExpVinho.csv"

# Ler os dados do arquivo CSV  ExpEspumantes.csv | ExpUva.csv | ExpSuco.csv
dados_exportacao = read_from_csv('ExpVinho.csv')

# Processar os dados
dados_processados = process_export_data(dados_exportacao)

# Exibir os dados processados
print(dados_processados)
"""
