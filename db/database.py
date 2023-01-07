from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta

from config.env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL: str = (
    "postgresql+psycopg2://"
    + f"{DB_USER}:"
    + f"{DB_PASSWORD}@"
    + f"{DB_HOST}:"
    + f"{DB_PORT}/"
    + f"{DB_NAME}"
)

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base: DeclarativeMeta = declarative_base()
