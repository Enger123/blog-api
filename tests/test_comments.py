from fastapi.testclient import TestClient
import pytest

@pytest.mark.parametrize(
    argnames='post_id, payload, exp_exception',
    argvalues=[
        [99999, {'text': 'Привіт'}, 404],
        [1, {'text': ''}, 422],
        [1, {'text': None}, 422],
    ]
)
def test_add_comments(
        test_client: TestClient,
        token,
        post_id,
        payload,
        exp_exception

):
    response = test_client.post(f"/posts/{post_id}/comments",
                                json=payload,
                                headers={
                                    "Authorization": f"Bearer {token}"
                                }
                                )
    comment_body = response.json()
    print(comment_body)
    assert response.status_code == exp_exception

def test_get_comments(test_client: TestClient, test_post):
    response = test_client.get(f"/posts/{test_post['id']}/comments")
    assert response.status_code == 200
    comments_body = response.json()
    assert isinstance(comments_body, list)

def test_change_comments(test_client: TestClient, token, test_comments):
    response = test_client.put(f"/comments/{test_comments['id']}",
                               json={
                                   'text': 'Змінений коментарій'
                               },
                               headers={
                                   'Authorization': f"Bearer {token}"
                               }
                               )
    print(response.json())
    assert response.status_code == 200
    com_body = response.json()
    assert isinstance(com_body, dict)

def test_change_comments_with_other_user(
        test_client: TestClient,
        test_user,
        test_user2,
        token2,
        test_comments
                                         ):
    response = test_client.put(f"comments/{test_comments['id']}",
        json={'text': 'Зміна'},
        headers={'Authorization': f"Bearer {token2}"})
    assert response.status_code == 404


def test_delete_comments(test_client: TestClient, token, test_comments):
    response = test_client.delete(f"/comments/{test_comments['id']}",
                               headers={
                                   'Authorization': f"Bearer {token}"
                               }
                               )
    assert response.status_code == 200
    com_body = response.json()
    assert com_body['message'] == 'Comment deleted'

