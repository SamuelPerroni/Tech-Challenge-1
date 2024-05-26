# Description: Pipeline for the Producao dataset.
# The pipeline is responsible for reading the dataset, cleaning it, transforming it and saving it to the database.


from pandas import DataFrame
from data.Producao import nodes


def producao_pipeline(path: str) -> DataFrame:
    df = nodes.read_from_csv(path)
    df = nodes.unpivot_years_columns(df)
    df = nodes.new_col_type(df)
 
    return df
