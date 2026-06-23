
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACESS_TOKEN_EXPIRE_MINUTES:int
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str
    JWT_SECRET_KEY:str

    class Config:
        env_file=".env"
        env_file_encoding = "utf-8"
settings =Settings()