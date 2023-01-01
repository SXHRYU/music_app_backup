from sqlalchemy.orm import Session

from . import models, schemas


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def get_songs(db: Session):
    return db.query(models.Song).all()

def add_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(id=song.id, name=song.name)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
