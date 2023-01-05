from os import environ

# production
DB_USER: str = str(environ["DB_USER"])
DB_PASSWORD: str = str(environ["DB_PASSWORD"])
DB_PORT: int = int(environ["DB_PORT"])
DB_HOST: str = str(environ["DB_HOST"])
DB_NAME: str = str(environ["DB_NAME"])
