import pytest
from fastapi.testclient import TestClient
from auth.jwt import hash_password

def test_post_users(test_client: TestClient):
    response = test_client.post("/users",
                                json={
                                    'username': 'Вот7',
                                    'password': '123456'
                                },
                                )
    post_body = response.json()
    assert response.status_code == 200
    assert isinstance(post_body, dict)

def test_get_users(test_client: TestClient):
    response = test_client.get("/users")
    assert response.status_code == 200

def test_get_user_id(test_client: TestClient, test_user):
    response = test_client.get(f"/users/{test_user['id']}")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data['id'] == test_user['id']

def test_get_user_id_wrong(test_client: TestClient, test_user, test_user2):
    response = test_client.get(f"/users/{test_user2['id']}")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['id'] != test_user['id']

def test_change_user(test_client: TestClient, token):
    response = test_client.put(f"/users",
                               json={
                                   'username': 'Змінено',
                                   'password': None
                               },
                               headers={
                                   'Authorization': f'Bearer {token}'
                               }
                               )
    assert response.status_code == 200
    user_body = response.json()
    assert 'Змінено' in user_body['username']

@pytest.mark.parametrize(
    argnames='payload, expected_username, expected_password',
    argvalues=[
        [{'username': 'Зміна', 'password': None}, 'Зміна', '123456'],
        [{'username': None, 'password': '123123'}, 'test_user', '123123'],
        [{'username': None, 'password': None}, 'test_user', '123456']
    ]
)
def test_parametrized_change_user(
        test_client: TestClient,
        test_user,
        token,
        payload,
        expected_username,
        expected_password
):
    response = test_client.put(f"/users",
                               json=payload,
                               headers={'Authorization': f'Bearer {token}'}
                               )
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['username'] == expected_username

def test_delete_user(test_client: TestClient, token):
    response = test_client.delete("/users",
                                  headers={
                                      'Authorization': f'Bearer {token}'
                                  })
    assert response.status_code == 200

def test_delete_user_with_invalid_token(test_client: TestClient, token):
    response = test_client.delete("/users",
                                  headers={
                                      'Authorization': f'Bearer asfafasff'
                                  })
    assert response.status_code == 401

