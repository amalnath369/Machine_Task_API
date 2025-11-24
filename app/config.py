from pydantic_settings import BaseSettings
from pydantic import AnyUrl



class Settings(BaseSettings):

    TITLE: str = "Machine Task"
    ENVIRONMENT: str = "dev"

    SECRET_KEY: str = "qwer"

    ALGORITHM: str = "HS256"

    DEBUG: bool = False

    DATABASE_URL : AnyUrl = 'sqlite+aiosqlite:///./test.db'

    ACCESS_TOKEN_EXPIRE_MINIUTES: int =30

    class Config:
        env_file = '.env'


settings = Settings()