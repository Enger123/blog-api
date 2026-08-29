from fastapi.testclient import TestClient

def test_stats_posts_count(test_client: TestClient):
    response = test_client.get("/stats/posts-count")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert 'Post_counter' in data