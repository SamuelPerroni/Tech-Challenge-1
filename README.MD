# Como rodar
1. Tenha o docker instalado na sua maquina.
2. Cria um arquivo .env dentro de TECH-CHALLENGE-1 (mesmo nivel do dockefile e doccker-compose.yml) com as seguintes variaveis:
- MYSQL_DATABASE
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_ROOT_PASSWORD
3. Rode no terminal docker-compose up --build
4. Acesse http://127.0.0.1:8000/docs#/
5. Depois de finalizar, rode docker-compose down

# Project

- Este projeto disponibiliza dados tratados de Vitivinicultura adquiridos pela Embrapa (https://vitibrasil.cnpuv.embrapa.br/).
- Há dois packages gerais:
    - /api
    - /data


# Packages 

## data
- O Package data é responsável pela busca de dados no site da embrapa, fazendo o download dos arquivos CSV e tratamento de dados.
- O package é separado em subpackages, cada um relacionado a cada fonte de dados.

1. Comercio
2. Exportacao
3. Importacao
4. Processamento
5. Producao

- Cada subpackage é responsável pela implementação dos seus nós (nodes.py) e seu pipeline (pipeline.py)

## api
- O package da API tem uma implementação semelhante ao data.
- É formado pelos subpackages

1. Comercio
2. Exportacao
3. Importacao
4. Processamento
5. Producao
6. security 

- Cada package é responsável pela criação do seu ORM (models.py), tipagem de de endpoints (schemas.py) e endpoint (routes.py) seguindo a mesma forma de implementação.
- O package security nos da a implementação de usuarios e autenticação via token JWT para ser usada nos demais packages.


# Funcionamento dos End Points

## Post Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: Post Requisition: Data
    API->>API: Check if object exists
    activate DB
    API->>+DB: Check if object exists
    alt Object Exists
        DB-->>API: Object Found
        API-->>Client: Status code = 409 (Conflict)
    else Object Does Not Exist
        DB-->>API: Object Not Found
        API->>+DB: Create object
        DB-->>API: Object Created
        API-->>Client: Status code = 200 (OK)
    end
    deactivate DB
```

## Get Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: Get Request
    API->>+DB: Retrieve Object
    alt Object Found
        DB-->>API: Object Data
        API-->>Client: Object Data
    else Object Not Found
        DB-->>API: Object Not Found
        API-->>Client: Status code = 404 (Not Found)
    end
```

## Put Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: Put Request: Updated Data
    API->>+DB: Check if Object Exists
    alt Object Exists
        DB-->>API: Object Found
        API->>+DB: Update Object
        DB-->>API: Object Updated
        API-->>Client: Status code = 200 (OK)
    else Object Does Not Exist
        DB-->>API: Object Not Found
        API-->>Client: Status code = 404 (Not Found)
    end
```

## DELETE Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: Delete Request
    API->>+DB: Check if Object Exists
    alt Object Exists
        DB-->>API: Object Found
        API->>+DB: Delete Object
        DB-->>API: Object Deleted
        API-->>Client: Status code = 200 (OK)
    else Object Does Not Exist
        DB-->>API: Object Not Found
        API-->>Client: Status code = 404 (Not Found)
    end
```

## Get or Create Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: GetOrCreate Request
    API->>+DB: Check if Object Exists
    alt Object Exists
        DB-->>API: Object Found
        API-->>Client: Object Data
    else Object Does Not Exist
        DB-->>API: Object Not Found
        API->>+DB: Create Object
        DB-->>API: Object Created
        API-->>Client: Newly Created Object Data
    end
```

## Create or Update Endpoint
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>+API: CreateOrUpdate Request: Data
    API->>+DB: Check if Object Exists
    alt Object Exists
        DB-->>API: Object Found
        API->>+DB: Update Object with Data
        DB-->>API: Object Updated
        API-->>Client: Status code = 200 (OK)
    else Object Does Not Exist
        DB-->>API: Object Not Found
        API->>+DB: Create Object with Data
        DB-->>API: Object Created
        API-->>Client: Status code = 201 (Created)
    end
```