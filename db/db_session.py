from sqlalchemy import create_engine,URL
from config.config import settings

db_config = {
    "drivername":settings.DRIVER_NAME,
    "username":settings.USER_NAME,
    "password":settings.PASSWORD,
    "host":settings.HOST,
    "port":settings.PORT_DB,
    "database":settings.DATABASE_DB
}

url_db=URL.create(**db_config)

engine=create_engine(url_db)