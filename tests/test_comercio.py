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
        assert 'comercio' in tables_names


@pytest.mark.asyncio
async def test_if_health_status_endpoint_returns_status_ok(create_test_client):
    test_client = create_test_client

    response = test_client.get("/health")


@pytest.mark.asyncio
async def test_if_faker_generates_an_object(create_fake_data):
    from api.comercio.models import Comercio
    obj = create_fake_data()
    assert Comercio(**obj.model_dump()) is not None


@pytest.mark.asyncio
async def test_if_post_endpoint_returns_status_ok_and_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    response_data = response.json()
    response_data.pop('id')
    assert response.status_code == 201
    assert response_data == comercio_data


@pytest.mark.asyncio
async def test_if_object_is_created_from_post_endpoint_by_reaching_get_endpoint_with_data(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data,  headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/comercio/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data

@pytest.mark.asyncio
async def test_if_object_is_duplicated_its_handle_by_the_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    _ = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    response_post = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    
    assert response_post.status_code == 409

@pytest.mark.asyncio
async def test_if_get_endpoint_returns_an_empty_list_if_there_are_no_objs_in_db(create_test_client, create_and_drop_db_yield_engine):
    test_client = create_test_client

    response = test_client.get('/comercio')
    response_data = response.json()

    assert response_data == []


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_no_object_in_database_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data,  jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.put('/comercio/1', json=comercio_data, headers=jwt_token_fixture)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_id_put_endpoint_returns_the_object_that_was_updated(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()
    comercio_data2 = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    id = response.json()['id']
    response = test_client.put(f'/comercio/{id}', json=comercio_data2, headers=jwt_token_fixture)
    response_data = response.json()
    response_data.pop('id')

    assert response.status_code == 200
    assert comercio_data2 == response_data


@pytest.mark.asyncio
async def test_if_object_was_updated_in_database_by_put_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()
    comercio_data2 = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    id = response.json()['id']
    response = test_client.put(f'/comercio/{id}', json=comercio_data2, headers=jwt_token_fixture)
    response_data_put = response.json()

    response = test_client.get('/comercio')
    response_data_get = response.json()

    assert response_data_put == response_data_get[0]


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_ok(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    id = response.json()['id']

    response = test_client.delete(f'/comercio/{id}', headers=jwt_token_fixture)

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_if_delete_endpoint_returns_status_404_if_no_data_to_delete(create_test_client, create_and_drop_db_yield_engine,  jwt_token_fixture):
    test_client = create_test_client
    response = test_client.delete(f'/comercio/{1}', headers=jwt_token_fixture)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_delete_endpoint_deletes_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.post('/comercio', json=comercio_data, headers=jwt_token_fixture)
    response_data = response.json()
    id = response_data['id']

    delete_response = test_client.delete(f'/comercio/{id}', headers=jwt_token_fixture)

    response = test_client.get('/comercio')
    response_data_get = response.json()

    assert len(response_data_get) == 0
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_if_get_or_create_creates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()

    response = test_client.post('/comercio/get-or-create/', json=comercio_data, headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/comercio/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data

@pytest.mark.asyncio
async def test_if_create_or_update_updates_an_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data, jwt_token_fixture):
    test_client = create_test_client
    comercio_data = create_fake_data().model_dump()
    comercio_data2 = comercio_data.copy()
    comercio_data2['commerce'] = 0.0

    _ = test_client.post('/comercio/create-or-update/', json=comercio_data, headers=jwt_token_fixture)

    response = test_client.post('/comercio/create-or-update/', json=comercio_data2, headers=jwt_token_fixture)
    response_data = response.json()

    response2 = test_client.get(f'/comercio/{response_data['id']}')
    response2_data = response2.json()

    assert response_data == response2_data
    response_data.pop('id')
    assert response_data == comercio_data2


@pytest.mark.asyncio
async def test_if_post_endpoint_addd_all_data(create_test_client, create_and_drop_db_yield_engine, run_pipeline, jwt_token_fixture):
    test_client = create_test_client
    data = run_pipeline
    responses = []
    for i in data.to_dict('records'):
        response = test_client.post('/comercio/', json=i, headers=jwt_token_fixture)
        responses.append(response.status_code)
    
    assert all(element == 201 for element in responses) is True
    