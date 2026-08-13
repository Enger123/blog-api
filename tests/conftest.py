from fastapi.testclient import TestClient
import pytest
from tests.database import *
from app.main import app
from sqlalchemy import text

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope='session',autouse=True)
async def create_tables():
    async with test_db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_db.dispose()

@pytest.fixture(autouse=True)
async def clean_database():
    yield

    async with test_db.begin() as conn:
        await conn.execute(text("""
                    TRUNCATE TABLE
                        comments,
                        likes,
                        posts,
                        tags,
                        users
                    RESTART IDENTITY CASCADE
                """))

# @pytest.fixture

@pytest.fixture
def test_user(test_client: TestClient):
    user_response = test_client.post("/users",
                                json={
                                    'username': 'test_user',
                                    'password': '123456'
                                },
                                )
    assert user_response.status_code == 200
    return user_response.json()

@pytest.fixture
def test_user2(test_client: TestClient):
    user_response = test_client.post("/users",
                                json={
                                    'username': 'test_user2',
                                    'password': '123456'
                                },
                                )
    assert user_response.status_code == 200
    return user_response.json()


@pytest.fixture
def token(test_client, test_user):
    login = test_client.post("/token",
                             data={
                                 'username': test_user['username'],
                                 'password': '123456'
                             }
                             )
    assert login.status_code == 200
    return login.json()['access_token']

@pytest.fixture
def token2(test_client, test_user2):
    login = test_client.post("/token",
                             data={
                                 'username': test_user2['username'],
                                 'password': '123456'
                             }
                             )
    assert login.status_code == 200
    return login.json()['access_token']

@pytest.fixture
def test_post(test_client: TestClient, token):
    post_response = test_client.post("/posts",
                                         json={
                                             'title': 'test post',
                                             'content': 'test content'
                                         },
                                         headers={
                                             'Authorization': f"Bearer {token}"
                                         }
                                         )
    assert post_response.status_code == 200
    return post_response.json()

@pytest.fixture
def test_comments(test_client: TestClient, token, test_post):
    com_response = test_client.post(f"/posts/{test_post['id']}/comments",
                                json={
                                    'text': 'Привіт'
                                },
                                headers={
                                    "Authorization": f"Bearer {token}"
                                }
                                )
    comment_body = com_response.json()
    print(comment_body)
    assert com_response.status_code == 200
    assert isinstance(comment_body, dict)
    return com_response.json()

@pytest.fixture
def test_tag(test_client: TestClient):
    response = test_client.post("/tags",
                                json=
                                {
                                    'name': 'Python test tag'
                                }
                                )
    assert response.status_code == 200
    assert response.json()['name'] == 'Python test tag'
    return response.json()
