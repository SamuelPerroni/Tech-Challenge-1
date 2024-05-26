from api import engine
import pytest


def get_table_names(conn):
    from sqlalchemy.inspection import inspect

    inspector = inspect(conn)
    return inspector.get_table_names()


@pytest.mark.asyncio
async def test_if_setup_works_and_create_tables_then_teardown(create_and_drop_db_yield_engine):
    engine = create_and_drop_db_yield_engine

    async with engine.begin() as conn:
        tables_names = await conn.run_sync(get_table_names)
        assert 'importacao' in tables_names


@pytest.mark.asyncio
async def test_if_health_status_endpoint_returns_status_ok(create_test_client):
    test_client = create_test_client

    response = test_client.get("/health")


@pytest.mark.asyncio
async def test_if_faker_generates_an_object(create_fake_data_importacao):
    from api.importacao.models import Importacao
    obj = create_fake_data_importacao()
    assert Importacao(**obj.model_dump()) is not None


@pytest.mark.asyncio
async def test_if_post_endpoint_returns_status_ok_and_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao,create_fake_data_user):
    
    test_client = create_test_client

    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}
    
    importacao_data = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=importacao_data, headers=header)
    response_data = response.json()
    response_data.pop('id')
    assert response.status_code == 201
    assert response_data == importacao_data


@pytest.mark.asyncio
async def test_if_object_is_created_from_post_endpoint_by_reaching_get_endpoint_with_data(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao,create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}
    
    importacao_data = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=importacao_data, headers=header)
    response_data = response.json()

    response2 = test_client.get(f'/importacao/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data


@pytest.mark.asyncio
async def test_if_object_is_duplicated_its_handle_by_the_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao,create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    importacao_data = create_fake_data_importacao().model_dump()

    _ = test_client.post('/importacao', json=importacao_data, headers=header)
    response_post = test_client.post('/importacao', json=importacao_data, headers=header)
    
    assert response_post.status_code == 409


@pytest.mark.asyncio
async def test_if_get_endpoint_returns_an_empty_list_if_there_are_no_objs_in_db(create_test_client, create_and_drop_db_yield_engine):
    test_client = create_test_client

    response = test_client.get('/importacao')
    response_data = response.json()

    assert response_data == []


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_no_object_in_database_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    importacao_data = create_fake_data_importacao().model_dump()

    response = test_client.put('/importacao/1', json=importacao_data, headers=header)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_id_put_endpoint_returns_the_object_that_was_updated(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    importacao_data = create_fake_data_importacao().model_dump()
    importacao_data2 = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=importacao_data, headers=header)
    id = response.json()['id']
    response = test_client.put(f'/importacao/{id}', json=importacao_data2, headers=header)
    response_data = response.json()
    response_data.pop('id')

    assert response.status_code == 200
    assert importacao_data2 == response_data


@pytest.mark.asyncio
async def test_if_object_was_updated_in_database_by_put_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    importacao_data = create_fake_data_importacao().model_dump()
    importacao_data2 = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=importacao_data, headers=header)
    id = response.json()['id']
    response = test_client.put(f'/importacao/{id}', json=importacao_data2, headers=header)
    response_data_put = response.json()

    response = test_client.get('/importacao')
    response_data_get = response.json()

    assert response_data_put == response_data_get[0]


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_ok(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    comercio_data_importacao = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=comercio_data_importacao, headers=header)
    id = response.json()['id']

    response = test_client.delete(f'/importacao/{id}', headers=header)

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_404_if_no_data_to_delete(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    response = test_client.delete(f'/importacao/{1}', headers=header)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_delete_endpoint_deletes_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    comercio_data_importacao = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao', json=comercio_data_importacao, headers=header)
    response_data = response.json()
    id = response_data['id']

    delete_response = test_client.delete(f'/importacao/{id}', headers=header)

    response = test_client.get('/importacao')
    response_data_get = response.json()

    assert len(response_data_get) == 0
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_if_get_or_create_creates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    comercio_data_importacao = create_fake_data_importacao().model_dump()

    response = test_client.post('/importacao/get-or-create/', json=comercio_data_importacao, headers=header)
    response_data = response.json()

    response2 = test_client.get(f'/importacao/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data

@pytest.mark.asyncio
async def test_if_create_or_update_updates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    importacao_data = create_fake_data_importacao().model_dump()
    importacao_data2 = importacao_data.copy()
    importacao_data2['valor'] = 0.0

    _ = test_client.post('/importacao/create-or-update/', json=importacao_data, headers=header)

    response = test_client.post('/importacao/create-or-update/', json=importacao_data2, headers=header)
    response_data = response.json()

    response2 = test_client.get(f'/importacao/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data
    response_data.pop('id')
    assert response_data == importacao_data2


@pytest.mark.asyncio
async def test_if_post_endpoint_addd_all_data(create_test_client, create_and_drop_db_yield_engine, run_pipeline_importacao, create_fake_data_user):
    test_client = create_test_client
    
    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    data = run_pipeline_importacao
    responses = []
    for i in data.to_dict('records'):
        response = test_client.post('/importacao/', json=i, headers=header)
        responses.append(response.status_code)
    
    assert all(element == 201 for element in responses) is True
    