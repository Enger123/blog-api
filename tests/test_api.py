# import pytest
# from fastapi.testclient import TestClient
#
# def test_post_users(test_client: TestClient):
#     response = test_client.post("/users",
#                                 json={
#                                     'username': 'Вот6',
#                                     'password': '123456'
#                                 },
#                                 )
#     post_body = response.json()
#     assert response.status_code == 200
#     assert isinstance(post_body, dict)
#
# def test_get_users(test_client: TestClient):
#     response = test_client.get("/users")
#     assert response.status_code == 200
#     assert len(response.json()) > 1
#
# def test_get_posts(test_client: TestClient):
#     response = test_client.get("/posts")
#     assert response.status_code == 200
#     assert len(response.json()) == 0
#
#
