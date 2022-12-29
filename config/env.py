from os import getenv


DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_PORT = int(getenv("DB_PORT"))
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
