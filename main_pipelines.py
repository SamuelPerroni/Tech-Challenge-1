# data lib
from data import (
    comercio_pipeline,
    processamento_pipeline,
    exportacao_pipeline,
    importacao_pipeline,
    producao_pipeline
)

# const
from const import (
    comercio_url,
    processamento_urls,
    exportacao_urls,
    importacao_urls,
    producao_url
)

if __name__ == '__main__':
  # print(comercio_pipeline(comercio_url).to_dict('records')[0])
  # processamento_pipeline(processamento_urls)
  # exportacao_pipeline(exportacao_urls)
  # importacao_pipeline(importacao_urls)
  # print(producao_pipeline(producao_url).to_dict('records')[0])
