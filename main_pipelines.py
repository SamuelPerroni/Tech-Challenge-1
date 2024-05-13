from data import comercio_pipeline
from data import processamento_pipeline
from const import comercio_url
from const import processamento_urls


if __name__ == '__main__':

    data = processamento_pipeline(processamento_urls).head(2)
    print(data.to_dict('records'))
    print(data.info())