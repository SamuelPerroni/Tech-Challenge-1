from pandas import DataFrame
from data.Exportacao import nodes


def exportacao_pipeline(path: str) -> DataFrame:
    df = nodes.read_from_csv(path)
    df = nodes.process_export_data(df)

    return df
