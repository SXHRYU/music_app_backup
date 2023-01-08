from sqlalchemy.orm import Session

from . import models, schemas


def get_song(db: Session, song_id: int) -> models.Song | None:
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def get_songs(db: Session) -> list[models.Song] | None:
    return db.query(models.Song).all()


def add_song(db: Session, song: schemas.SongCreate) -> models.Song:
    db_song: models.Song = models.Song(id=song.id, name=song.name, path=song.path)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
