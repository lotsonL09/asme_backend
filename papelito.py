from sqlalchemy import create_engine,URL
from config.config import settings

db_config = {
    "drivername":settings.DRIVER_NAME,
    "username":settings.USER_NAME,
    "password":settings.PASSWORD_DB,
    "host":settings.HOST_NAME,
    "port":settings.PORT_DB,
    "database":settings.DATABASE_DB
}

print(db_config)