from data import comercio_pipeline
from const import comercio_url


if __name__ == '__main__':

    print(comercio_pipeline(comercio_url).info())
