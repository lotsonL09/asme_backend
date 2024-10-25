from pydantic import NonNegativeInt
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SECRET_KEY:str

    DRIVER_NAME:str
    USERNAME:str
    PASSWORD:str
    HOST:str
    PORT:NonNegativeInt
    DATABASE:str

    class Config:
        env_file=".env"

settings=Settings()