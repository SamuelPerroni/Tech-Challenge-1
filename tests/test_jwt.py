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
async def test_if_create_endpoint_returns_status_ok_and_the_object(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()

    response = test_client.post('/jwt/create', json=user_data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data['user_name'] == user_data['user_name']


@pytest.mark.asyncio
async def test_if_object_is_created_from_post_endpoint_by_reaching_get_endpoint_with_data(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()

    response = test_client.post('/jwt/create', json=user_data)
    response_data = response.json()

    response2 = test_client.get(f'/jwt/{response_data['user_name']}')
    response2_data = response2.json()

    assert response_data == response2_data


@pytest.mark.asyncio
async def test_if_object_is_duplicated_its_handle_by_the_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()

    _ = test_client.post('/jwt/create', json=user_data)
    response_post = test_client.post('/jwt/create', json=user_data)
    
    assert response_post.status_code == 409


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_no_user_name_in_database_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()
    
    response_post = test_client.post('/jwt/create', json=user_data)
    response_data = response_post.json()

    user_data_update = {'user_name': 'angelo', 'user_pass': user_data['user_pass']}
    user_data_update.update({'new_user_name': user_data['user_name']})
    user_data_update.update({'new_user_pass': user_data['user_pass']})
    print(user_data_update)
    response = test_client.put('/jwt/', json=user_data_update)
    print(response.status_code)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_put_endpoint_returns_error_if_password_is_wrong_to_update(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()
    
    response_post = test_client.post('/jwt/create', json=user_data)
    response_data = response_post.json()

    user_data_update = {'user_name': user_data['user_name'], 'user_pass': '123'}
    user_data_update.update({'new_user_name': user_data['user_name']})
    user_data_update.update({'new_user_pass': user_data['user_pass']})
    print(user_data_update)
    response = test_client.put('/jwt/', json=user_data_update)
    print(response.status_code)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_if_put_endpoint_is_updating_user(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    user_data = create_fake_data_user().model_dump()
    
    response_post = test_client.post('/jwt/create', json=user_data)
    response_data = response_post.json()

    user_data_update = {'user_name': user_data['user_name'], 'user_pass': user_data['user_pass']}
    user_data_update.update({'new_user_name': 'Angelo'})
    user_data_update.update({'new_user_pass': 'Angelo123'})
    print(user_data_update)
    response = test_client.put('/jwt/', json=user_data_update)
    codigo1 = response.status_code
    
    user_data_test = {'user_name': user_data['user_name'], 'user_pass': user_data['user_pass']}
    response = test_client.put('/jwt/', json=user_data_test)
    codigo2 = response.status_code

    user_data_test = {'user_name': 'Angelo', 'user_pass': 'Angelo123'}
    response = test_client.put('/jwt/', json=user_data_test)
    codigo3 = response.status_code

    assert codigo1 == 200
    assert codigo2 == 404
    assert codigo3 == 200

@pytest.mark.asyncio
async def test_delete_endpoint(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    data_user = create_fake_data_user().model_dump()

    response = test_client.post('/jwt/create', json=data_user)

    response_get = test_client.get(f'/jwt/{data_user['user_name']}')
    response_get_data = response_get.json()


    response = test_client.delete(f'/jwt?user_name={data_user['user_name']}&user_pass={data_user['user_pass']}')


    response_get2 = test_client.get(f'/jwt/{data_user['user_name']}')
    response_get2_data = response_get2.json()

    assert response.status_code == 200
    assert response_get.status_code == 200
    assert response_get2.status_code == 404

@pytest.mark.asyncio
async def test_create_token(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
    test_client = create_test_client
    data_user = create_fake_data_user().model_dump()

    response = test_client.post('/jwt/create', json=data_user)

    response = test_client.post('/jwt/token', json=data_user)

    token = response.json()
    assert 'access_token' in token
    assert 'token_type' in token

    data_user_different = {'user_name': data_user['user_name'], 'user_pass': 'senha'}
    response = test_client.post('/jwt/token', json=data_user_different)

    assert response.status_code == 404

    data_user_different = {'user_name': 'hahaha', 'user_pass': data_user['user_pass']}
    response = test_client.post('/jwt/token', json=data_user_different)

    assert response.status_code == 404

# @pytest.mark.asyncio
# async def test_token_request(create_test_client, create_and_drop_db_yield_engine, create_fake_data_user):
#     test_client = create_test_client
#     data_user = create_fake_data_user().model_dump()

#     response = test_client.post('/jwt/create', json=data_user)
#     response = test_client.post('/jwt/token', json=data_user)

#     token = response.json()['access_token']
#     header = {'Authorization': f'Bearer {token}'}

#     response2 = test_client.get(f'/jwt/testToken/{data_user['user_name']}', headers=header)
#     assert response2.status_code == 200

#     header = {'Authorization': f'Bearer {token}ab'}
#     response2 = test_client.get(f'/jwt/testToken/{data_user['user_name']}', headers=header)
#     assert response2.status_code == 401

#     header = {'Authorization': f'abc'}
#     response2 = test_client.get(f'/jwt/testToken/{data_user['user_name']}', headers=header)
#     assert response2.status_code == 403





