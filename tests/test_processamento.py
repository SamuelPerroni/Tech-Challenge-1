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
        assert 'processamento' in tables_names


@pytest.mark.asyncio
async def test_if_health_status_endpoint_returns_status_ok(create_test_client):
    test_client = create_test_client

    response = test_client.get("/health")


@pytest.mark.asyncio
async def test_if_faker_generates_an_object(create_fake_data_processamento):
    from api.processamento.models import Processamento
    obj = create_fake_data_processamento()
    assert Processamento(**obj.model_dump()) is not None


@pytest.mark.asyncio
async def test_if_post_endpoint_returns_status_ok_and_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=processamento_data)
    response_data = response.json()
    response_data.pop('id')
    assert response.status_code == 201
    assert response_data == processamento_data


@pytest.mark.asyncio
async def test_if_object_is_created_from_post_endpoint_by_reaching_get_endpoint_with_data(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=processamento_data)
    response_data = response.json()

    response2 = test_client.get(f'/processamento/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data


@pytest.mark.asyncio
async def test_if_object_is_duplicated_its_handle_by_the_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()

    _ = test_client.post('/processamento', json=processamento_data)
    response_post = test_client.post('/processamento', json=processamento_data)
    
    assert response_post.status_code == 409


@pytest.mark.asyncio
async def test_if_get_endpoint_returns_an_empty_list_if_there_are_no_objs_in_db(create_test_client, create_and_drop_db_yield_engine):
    test_client = create_test_client

    response = test_client.get('/processamento')
    response_data = response.json()

    assert response_data == []


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_no_object_in_database_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()

    response = test_client.put('/processamento/1', json=processamento_data)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_id_put_endpoint_returns_the_object_that_was_updated(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()
    processamento_data2 = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=processamento_data)
    id = response.json()['id']
    response = test_client.put(f'/processamento/{id}', json=processamento_data2)
    response_data = response.json()
    response_data.pop('id')

    assert response.status_code == 200
    assert processamento_data2 == response_data


@pytest.mark.asyncio
async def test_if_object_was_updated_in_database_by_put_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()
    processamento_data2 = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=processamento_data)
    id = response.json()['id']
    response = test_client.put(f'/processamento/{id}', json=processamento_data2)
    response_data_put = response.json()

    response = test_client.get('/processamento')
    response_data_get = response.json()

    assert response_data_put == response_data_get[0]


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_ok(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    comercio_data_processamento = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=comercio_data_processamento)
    id = response.json()['id']

    response = test_client.delete(f'/processamento/{id}')

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_404_if_no_data_to_delete(create_test_client, create_and_drop_db_yield_engine):
    test_client = create_test_client
    response = test_client.delete(f'/processamento/{1}')

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_delete_endpoint_deletes_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    comercio_data_processamento = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento', json=comercio_data_processamento)
    response_data = response.json()
    id = response_data['id']

    delete_response = test_client.delete(f'/processamento/{id}')

    response = test_client.get('/processamento')
    response_data_get = response.json()

    assert len(response_data_get) == 0
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_if_get_or_create_creates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    comercio_data_processamento = create_fake_data_processamento().model_dump()

    response = test_client.post('/processamento/get-or-create/', json=comercio_data_processamento)
    response_data = response.json()

    response2 = test_client.get(f'/processamento/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data

@pytest.mark.asyncio
async def test_if_create_or_update_updates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_processamento):
    test_client = create_test_client
    processamento_data = create_fake_data_processamento().model_dump()
    processamento_data2 = processamento_data.copy()
    processamento_data2['commerce'] = 0.0

    _ = test_client.post('/processamento/create-or-update/', json=processamento_data)

    response = test_client.post('/processamento/create-or-update/', json=processamento_data2)
    response_data = response.json()

    response2 = test_client.get(f'/processamento/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data
    response_data.pop('id')
    assert response_data == processamento_data2


@pytest.mark.asyncio
async def test_if_post_endpoint_addd_all_data(create_test_client, create_and_drop_db_yield_engine, run_pipeline_processamento):
    test_client = create_test_client
    data = run_pipeline_processamento
    responses = []
    for i in data.to_dict('records'):
        response = test_client.post('/processamento/', json=i)
        responses.append(response.status_code)
    
    assert all(element == 201 for element in responses) is True
    