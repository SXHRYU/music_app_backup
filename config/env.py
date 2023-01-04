from os import getenv

# production
DB_USER: str = str(getenv("DB_USER"))
DB_PASSWORD: str = str(getenv("DB_PASSWORD"))
DB_PORT = int(getenv("DB_PORT"))
DB_HOST: str = str(getenv("DB_HOST"))
DB_NAME: str = str(getenv("DB_NAME"))
