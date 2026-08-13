import pytest
from fastapi.testclient import TestClient

def test_add_likes(test_client: TestClient, token, test_post):
    response1 = test_client.post(f"/posts/{test_post['id']}/like",
                                headers={
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response1.status_code == 200
    likes_body = response1.json()
    assert 'id' in likes_body

    response2 = test_client.post(f"/posts/{test_post['id']}/like",
                                headers={
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response2.status_code == 400

def test_get_likes_username(test_client: TestClient, test_post, token):
    response1 = test_client.post(f"/posts/{test_post['id']}/like",
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response1.status_code == 200
    response = test_client.get(f"/likes/test_")
    assert response.status_code == 200

def test_delete_like(test_client: TestClient, token, test_post):
    response_post_like = test_client.post(f"/posts/{test_post['id']}/like",
                                 headers={
                                     'Authorization': f"Bearer {token}"
                                 }
                                 )
    assert response_post_like.status_code == 200

    response = test_client.delete(f"/posts/{test_post['id']}/like",
                                  headers={
                                      'Authorization': f"Bearer {token}"
                                  }
                                  )
    data_body = response.json()
    assert response.status_code == 200
    assert isinstance(data_body, dict)
    assert data_body['message'] == 'Лайк прибрано'
