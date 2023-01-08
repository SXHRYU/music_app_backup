from typing import Any, BinaryIO, Generator

from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()


# Dependency
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/songs/{song_id}", response_model=schemas.SongCreate)
def get_song(song_id: int, db: Session = Depends(get_db)) -> Any:
    song: models.Song | None = crud.get_song(db, song_id)
    if not song:
        return JSONResponse(
            status_code=404, content={"message": "No song with such ID exists"}
        )
    else:
        headers: dict[str, str] = {"x-song-name": song.name}
        # response.headers["artist"] = song.artist
        return FileResponse(song.path, headers=headers)


@app.post("/songs/", status_code=201, response_model=schemas.Song)
def add_song(
    uploaded_song: UploadFile, request: Request, db: Session = Depends(get_db)
) -> schemas.Song:
    song_data: BinaryIO = uploaded_song.file
    song_name: str = request.headers["x-song-name"]

    song: schemas.SongCreate = schemas.SongCreate(
        id=-4, name=song_name, path=f"./music/test/{song_name}", data=song_data.read()
    )
    with open(song.path, "wb") as f:
        crud.add_song(db=db, song=song)
        f.write(song.data)
    return schemas.Song(**dict(song))
