from pathlib import Path
from typing import Generator

import psycopg2
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app, get_db
from config.test_env import (
    DB_HOST_test,
    DB_NAME_test,
    DB_PASSWORD_test,
    DB_PORT_test,
    DB_USER_test,
)
from db.database import Base

SQLALCHEMY_DATABASE_URL: str = (
    "postgresql+psycopg2://"
    + f"{DB_USER_test}:"
    + f"{DB_PASSWORD_test}@"
    + f"{DB_HOST_test}:"
    + f"{DB_PORT_test}/"
    + f"{DB_NAME_test}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def mock_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    conn = psycopg2.connect(
        host=DB_HOST_test,
        port=DB_PORT_test,
        dbname=DB_NAME_test,
        user=DB_USER_test,
        password=DB_PASSWORD_test,
    )
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO songs VALUES (%s, %s, %s);",
            (-1, "1.mp3", "./music/test/1.mp3"),
        )
        cur.execute(
            "INSERT INTO songs VALUES (%s, %s, %s);",
            (-2, "2.mp3", "./music/test/2.mp3"),
        )
        cur.execute(
            "INSERT INTO songs VALUES (%s, %s, %s);",
            (-3, "3.mp3", "./music/test/3.mp3"),
        )
        conn.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    try:
        db: Session = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_song_1(mock_db: Generator[None, None, None]) -> None:
    response = client.get("/songs/-1")
    assert response.status_code == 200
    assert response.content == open("./music/test/1.mp3", "rb").read()
    assert response.headers["x-song-name"] == "1.mp3"


def test_get_song_2(mock_db: Generator[None, None, None]) -> None:
    response = client.get("/songs/-2")
    assert response.status_code == 200
    assert response.content == open("./music/test/2.mp3", "rb").read()
    assert response.headers["x-song-name"] == "2.mp3"


def test_add_song(mock_db: Generator[None, None, None]) -> None:
    files = {
        "uploaded_song": open("tests/audio.mp3", "rb").read(),
    }
    headers = {"x-song-name": "4.mp3"}
    response = client.post("/songs/", files=files, headers=headers)
    assert response.status_code == 201
    assert response.json() == {
        "id": -4,
        "name": "4.mp3",
        "path": "./music/test/4.mp3",
    }
    assert Path(response.json()["path"]).exists()
    Path(response.json()["path"]).unlink(missing_ok=True)
