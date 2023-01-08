from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .database import Base


class Song(Base):
    __tablename__ = "songs"

    id: Column[Any] = Column("id", INTEGER, primary_key=True, index=True)
    name: Column[Any] = Column("name", VARCHAR(100), index=True, nullable=False)
    path: Column[Any] = Column("path", VARCHAR(100), nullable=False)
