from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_song_1():
    response = client.get("/songs/-1")
    assert response.status_code == 200
    assert response.json() == {
        "id": -1,
        "name": "goodo_1",
    }

def test_get_song_2():
    response = client.get("/songs/-2")
    assert response.status_code == 200
    assert response.json() == {
        "id": -2,
        "name": "goodo_2",
    }

