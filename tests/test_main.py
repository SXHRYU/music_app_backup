from pathlib import Path

import psycopg2
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from config.env import (DB_HOST_test, DB_NAME_test, DB_PASSWORD_test,
                        DB_PORT_test, DB_USER_test)
from db.database import Base

SQLALCHEMY_DATABASE_URL = (
                            f"postgresql+psycopg2://"
                            + f"{DB_USER_test}:"
                            + f"{DB_PASSWORD_test}@"
                            + f"{DB_HOST_test}:"
                            + f"{DB_PORT_test}/"
                            + f"{DB_NAME_test}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def mock_db():
    Base.metadata.create_all(bind=engine)
    conn = psycopg2.connect(
        host=DB_HOST_test,
        port=DB_PORT_test,
        dbname=DB_NAME_test,
        user=DB_USER_test,
        password=DB_PASSWORD_test,
    )
    with conn.cursor() as cur:
        cur.execute("INSERT INTO songs VALUES (%s, %s, %s);", (-1, "goodo_1", "./music/test/1.mp3"))
        cur.execute("INSERT INTO songs VALUES (%s, %s, %s);", (-2, "goodo_2", "./music/test/2.mp3"))
        cur.execute("INSERT INTO songs VALUES (%s, %s, %s);", (-3, "goodo_3", "./music/test/3.mp3"))
        conn.commit()
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_song_1(mock_db):
    response = client.get("/songs/-1")
    assert response.status_code == 200
    assert response.content == open("./music/test/1.mp3", 'rb').read()
    assert response.headers["x-song-name"] == "goodo_1"

def test_get_song_2(mock_db):
    response = client.get("/songs/-2")
    assert response.status_code == 200
    assert response.content == open("./music/test/2.mp3", 'rb').read()
    assert response.headers["x-song-name"] == "goodo_2"

# def test_get_all_songs(mock_db):
#     response = client.get("/songs/")
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             "id": -1,
#             "name": "goodo_1",
#              "path": "/music/07 The Stains of Time (Maniac Agenda Mix).mp3",
#         },
#         {
#             "id": -2,
#             "name": "goodo_2",
#             "path": "/music/08 Red Sun (Maniac Agenda Mix).mp3",
#         },
#         {
#             "id": -3,
#             "name": "goodo_3",
#             "path": "09 A Soul Can’t Be Cut (Platinum Mix).mp3",
#         },
#     ]

def test_add_song(mock_db):
    files = {
        "song": open("tests/audio.mp3", 'rb').read(),
    }
    headers = {
        "x-song-name": "4.mp3"
    }
    response = client.post("/songs/", files=files, headers=headers)
    assert response.status_code == 201
    assert response.json() == {
        "id": -4,
        "name": "4.mp3",
        "path": "./music/test/4.mp3",
    }
    assert Path(response.json()['path']).exists()
    Path(response.json()['path']).unlink(missing_ok=True)
