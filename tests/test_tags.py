import pytest
from fastapi.testclient import TestClient

#винести ф-ію зверху в conftest щоб додавати через ['id']
#і воно не залежало від даних в базі даних поточно створених

def test_get_created_tags(test_client: TestClient, test_tag):
    response = test_client.get("/tags")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert isinstance(data, list)
    assert data[0]['name'] == 'Python test tag'

def test_add_tag_inpost(test_client: TestClient, token, test_post, test_tag):
    response = test_client.post(f"/posts/{test_post['id']}/tags/{test_tag['id']}",
                                headers=
                                {
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response.status_code == 200

    response2 = test_client.post(f"/posts/{test_post['id']}/tags/10",
                                headers=
                                {
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response2.status_code == 404

    print(response.json())

def test_get_post_tags(test_client: TestClient, test_post, test_tag, token):
    response1 = test_client.post(f"/posts/{test_post['id']}/tags/{test_tag['id']}",
                                headers=
                                {
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response1.status_code == 200

    response2 = test_client.get(f"/posts/{test_post['id']}/tags")
    assert response2.status_code == 200

def test_delete_post_tags(test_client: TestClient, token, test_post, test_tag):
    response1 = test_client.post(f"/posts/{test_post['id']}/tags/{test_tag['id']}",
                                headers=
                                {
                                    'Authorization': f"Bearer {token}"
                                }
                                )
    assert response1.status_code == 200

    response1 = test_client.delete(f"/posts/{test_post['id']}/tags/{test_tag['id']}",
                                  headers={
                                      'Authorization': f'Bearer {token}'
                                  }
                                  )
    assert response1.status_code == 200


