from data import comercio_pipeline
from data import processamento_pipeline
from const import comercio_url
from const import processamento_urls


if __name__ == '__main__':

    print(comercio_pipeline(comercio_url).info())
