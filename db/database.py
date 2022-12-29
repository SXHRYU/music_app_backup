from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.env import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)

SQLALCHEMY_DATABASE_URL = (
                            f"postgresql+psycopg2://"
                            + f"{DB_USER}:"
                            + f"{DB_PASSWORD}@"
                            + f"{DB_HOST}:"
                            + f"{DB_PORT}/"
                            + f"{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
