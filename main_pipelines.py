from data import comercio_pipeline
from data import processamento_pipeline
from data import exportacao_pipeline
from const import comercio_url
from const import exportacao_urls
from const import processamento_urls


if __name__ == '__main__':

    print(comercio_pipeline(comercio_url).info())

    for x in processamento_urls:
        print(processamento_pipeline(x).info())

    for x in exportacao_urls:
        print(exportacao_pipeline(x).info())