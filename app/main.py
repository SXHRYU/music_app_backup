from typing import Any, Generator, BinaryIO

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

@app.get("/songs/{song_id}")
def get_song(song_id: int, db: Session = Depends(get_db)) -> FileResponse | JSONResponse:
    song: models.Song | None = crud.get_song(db, song_id)
    if not song:
        return JSONResponse(
            status_code=404,
            content={
                "message": "No song with such ID exists"
            }
        )
    else:
        headers: dict[str, Any] = {"x-song-name": song.name}
        # response.headers["artist"] = song.artist
        return FileResponse(song.path, headers=headers)

# @app.get("/songs/", response_model=list[schemas.Song])
# def get_all_songs(db: Session = Depends(get_db)):
#     songs = crud.get_songs(db)
#     return songs

@app.post("/songs/", status_code=201, response_model=schemas.Song)
def add_song(
    uploaded_song: UploadFile,
    request: Request,
    db: Session = Depends(get_db)
) -> schemas.Song:
    song_data: BinaryIO = uploaded_song.file
    song_name: str = request.headers["x-song-name"]

    song: schemas.SongCreate = schemas.SongCreate(id=-4,
                                                  name=song_name,
                                                  path=f"./music/test/{song_name}",
                                                  data=song_data.read())
    with open(song.path, 'wb') as f:
        crud.add_song(db=db, song=song)
        f.write(song.data)
    return schemas.Song(**dict(song))

# @app.post("/songs/", response_model=schemas.Song)
# def add_one_song(song: schemas.Song, db: Session = Depends(get_db)):
#     users = crud.add_song(db, song)
#     return users

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
