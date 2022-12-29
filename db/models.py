from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import (
    JSON,
    INTEGER,
    SMALLINT,
    UUID,
    VARCHAR,
)
from sqlalchemy.orm import relationship

from .database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column("id", INTEGER, primary_key=True, index=True)
    name = Column("name", VARCHAR(100), index=True, nullable=False)


# class Artist(Base):
#     __tablename__ = "artists"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

# class Album(Base):
#     __tablename__ = "albums"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
