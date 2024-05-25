import data.Producao
from const import producao_urls
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting pipeline')
    data.Producao.producao_pipeline(producao_urls[0])
    logging.info('Pipeline finished')


if __name__ == '__main__':
    main()
