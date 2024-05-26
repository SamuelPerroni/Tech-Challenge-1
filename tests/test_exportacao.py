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
        assert 'exportacao' in tables_names


@pytest.mark.asyncio
async def test_if_faker_generates_an_object(create_fake_data_exportacao):
    from api.exportacao.models import Exportacao
    obj = create_fake_data_exportacao()
    assert Exportacao(**obj.model_dump()) is not None


@pytest.mark.asyncio
async def test_if_post_endpoint_returns_status_ok_and_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, create_fake_data_user):
    test_client = create_test_client

    data_user = create_fake_data_user().model_dump()
    response = test_client.post('/jwt/create', json=data_user)
    response = test_client.post('/jwt/token', json=data_user)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}

    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data, headers=header)
    response_data = response.json()
    response_data.pop('id')
    assert response.status_code == 201
    assert response_data == exportacao_data


@pytest.mark.asyncio
async def test_if_object_is_created_from_post_endpoint_by_reaching_get_endpoint_with_data(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/exportacao/{response_data['id']}', )
    response2_data = response2.json()

    assert response_data == response2_data


@pytest.mark.asyncio
async def test_if_object_is_duplicated_its_handle_by_the_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao,  jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    _ = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    response_post = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    
    assert response_post.status_code == 409


@pytest.mark.asyncio
async def test_if_get_endpoint_returns_an_empty_list_if_there_are_no_objs_in_db(create_test_client, create_and_drop_db_yield_engine):
    test_client = create_test_client

    response = test_client.get('/exportacao')
    response_data = response.json()

    assert response_data == []


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_no_object_in_database_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.put('/exportacao/1', json=exportacao_data, headers=jwt_token_fixture)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_id_put_endpoint_returns_the_object_that_was_updated(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao,  jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()
    exportacao_data2 = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    id = response.json()['id']
    response = test_client.put(f'/exportacao/{id}', json=exportacao_data2,  headers=jwt_token_fixture)
    response_data = response.json()
    response_data.pop('id')

    assert response.status_code == 200
    assert exportacao_data2 == response_data


@pytest.mark.asyncio
async def test_if_object_was_updated_in_database_by_put_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()
    exportacao_data2 = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    id = response.json()['id']
    response = test_client.put(f'/exportacao/{id}', json=exportacao_data2,  headers=jwt_token_fixture)
    response_data_put = response.json()

    response = test_client.get('/exportacao')
    response_data_get = response.json()

    assert response_data_put == response_data_get[0]


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_ok(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data, headers=jwt_token_fixture)
    id = response.json()['id']

    response = test_client.delete(f'/exportacao/{id}', headers=jwt_token_fixture)

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_404_if_no_data_to_delete(create_test_client, create_and_drop_db_yield_engine,  jwt_token_fixture):
    test_client = create_test_client
    response = test_client.delete(f'/exportacao/{1}', headers=jwt_token_fixture)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_delete_endpoint_deletes_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao', json=exportacao_data,  headers=jwt_token_fixture)
    response_data = response.json()
    id = response_data['id']

    delete_response = test_client.delete(f'/exportacao/{id}', headers=jwt_token_fixture)

    response = test_client.get('/exportacao')
    response_data_get = response.json()

    assert len(response_data_get) == 0
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_if_get_or_create_creates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()

    response = test_client.post('/exportacao/get-or-create/', json=exportacao_data,  headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/exportacao/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data


@pytest.mark.asyncio
async def test_if_create_or_update_updates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_exportacao, jwt_token_fixture):
    test_client = create_test_client
    exportacao_data = create_fake_data_exportacao().model_dump()
    exportacao_data2 = exportacao_data.copy()
    exportacao_data2['valor'] = 0.0

    _ = test_client.post('/exportacao/create-or-update/', json=exportacao_data, headers=jwt_token_fixture)

    response = test_client.post('/exportacao/create-or-update/', json=exportacao_data2, headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/exportacao/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data
    response_data.pop('id')
    assert response_data == exportacao_data2


@pytest.mark.asyncio
async def test_if_post_endpoint_addd_all_data(create_test_client, create_and_drop_db_yield_engine, run_pipeline_exportacao,  jwt_token_fixture):
    test_client = create_test_client
    data = run_pipeline_exportacao
    responses = []
    for i in data.to_dict('records'):
        response = test_client.post('/exportacao/', json=i, headers=jwt_token_fixture)
        responses.append(response.status_code)
    
    assert all(element == 201 for element in responses) is True
    