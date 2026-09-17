from fastapi.testclient import TestClient
import pytest

def test_add_posts(test_client: TestClient, token):
    response = test_client.post("/posts",
                                json={
                                    'title': 'Тест Пост',
                                    'content': 'Тест контент',
                                },
                                headers={'Authorization': f"Bearer {token}"}
                                )
    assert response.status_code == 200
    post_body = response.json()
    print(post_body)
    assert isinstance(post_body, dict)


def test_get_posts(test_client: TestClient):
    response = test_client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.parametrize(
    argnames='payload, exp_title, exp_content',
    argvalues=[
        [{'title': 'Зміна', 'content': None}, 'Зміна', 'test content'],
        [{'title': None, 'content': 'Зміна'}, 'test post', 'Зміна'],
        [{'title': None, 'content': None}, 'test post', 'test content'],
        [{'title': 'Зміна'}, 'Зміна', 'test content'],
        [{'content': 'Зміна'}, 'test post', 'Зміна'],
        [{}, 'test post', 'test content'],
        [{'title': 'Зміна', 'content': 'Зміна'}, 'Зміна', 'Зміна']
    ]
)
def test_change_posts(
        test_client: TestClient,
        token,
        test_post,
        payload,
        exp_title,
        exp_content):
    response = test_client.put(f"/posts/{test_post['id']}",
                               json=payload,
                               headers={
                                   'Authorization': f"Bearer {token}"
                               }
                               )
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == exp_title
    assert data['content'] == exp_content

def test_my_posts(test_client: TestClient):
    response = test_client.get("/me/posts")
    assert response.status_code == 401

def test_delete_posts(test_client: TestClient, token, test_post):
    # post_response = test_client.post("/posts",
    #                             json={
    #                                 'title': 'Тест Пост',
    #                                 'content': 'Тест контент',
    #                             },
    #                             headers={'Authorization': f"Bearer {token}"}
    #                             )
    # assert post_response.status_code == 200
    # post_body = post_response.json()
    # assert isinstance(post_body, dict)

    delete_response = test_client.delete(f"/posts/{test_post['id']}", headers=
    {
     'Authorization': f"Bearer {token}"
    }
                                  )
    data = delete_response.json()
    assert delete_response.status_code == 200
    assert isinstance(data, dict)


