from os import getenv

# production
DB_USER: str = str(getenv("DB_USER"))
DB_PASSWORD: str = str(getenv("DB_PASSWORD"))
DB_PORT = int(getenv("DB_PORT"))
DB_HOST: str = str(getenv("DB_HOST"))
DB_NAME: str = str(getenv("DB_NAME"))

# testing
DB_USER_test: str = str(getenv("DB_USER_test"))
DB_PASSWORD_test: str = str(getenv("DB_PASSWORD_test"))
DB_PORT_test = int(getenv("DB_PORT_test"))
DB_HOST_test: str = str(getenv("DB_HOST_test"))
DB_NAME_test: str = str(getenv("DB_NAME_test"))
