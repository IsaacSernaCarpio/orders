
# python
from os import getenv
from os import getcwd

# dotenv
from dotenv import load_dotenv


# passlib
from passlib.context import CryptContext

# helpers
from libs.helpers.credentials import MySQLCredential

# start envs
load_dotenv()

PWD_CONTEXT = CryptContext(schemes=["argon2"])


# Obtener el directorio actual
BASE_PATH = getcwd()


# OTHERS
MINUTOS = int(getenv("SESSION_TIME"))
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')

ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

ENVIRONMENT = getenv('ENVIRONMENT')

MYSQL_CREDENTIAL = None

if ENVIRONMENT == 'dev':
    DEV_MYSQL_HOST = getenv('DEV_MYSQL_HOST')
    DEV_MYSQL_DB = getenv('DEV_MYSQL_DB')
    DEV_MYSQL_USER = getenv('DEV_MYSQL_USER')
    DEV_MYSQL_PASSWORD = getenv('DEV_MYSQL_PASSWORD')
    DEV_MYSQL_PORT = getenv('DEV_MYSQL_PORT')
    MYSQL_CREDENTIAL = MySQLCredential(
        _host=DEV_MYSQL_HOST,
        _db_name=DEV_MYSQL_DB,
        _user=DEV_MYSQL_USER,
        _password=DEV_MYSQL_PASSWORD,
        _port=DEV_MYSQL_PORT
    )
else:
    MYSQL_CREDENTIAL = MySQLCredential(
         _db_name='',
        _user='',
        _password='',
    )

print(f"\t> host: {MYSQL_CREDENTIAL.host.upper()} {ENVIRONMENT}")
PATH_WEB = getenv('PATH_WEB')
VAPID_PRIVATE_KEY = getenv('VAPID_PRIVATE_KEY')
VAPID_PUBLIC_KEY = getenv('VAPID_PUBLIC_KEY')